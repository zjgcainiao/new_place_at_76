

from django.http import JsonResponse
import json
from firebase_admin import auth
# 2023-10-13
# defined to verify a token from authenticated user via firebase auth javscript script.
# the script is defined in firebase_auth_register_and_sign_in_with_django.js that is serverd via static files via "{% static '' %}"
from django.contrib import messages
import time 
from firebase_auth_app.models import FirebaseUser
from asgiref.sync import sync_to_async
from firebase_auth_app.firebase_auth_backend import FirebaseAuthBackend

async def verify_firebase_token(request):
    if request.method == 'POST':
                # Access the raw JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # Handle JSON decoding error
            return JsonResponse({'error': 'Invalid firebase user JSON data'}, status=400)
        
        # Extract required data from the parsed JSON
        token = data.get('token')
        # decoded_token = auth.verify_id_token(token)
        decoded_token = await sync_to_async(auth.verify_id_token)(token)
        exp = decoded_token['exp']
        uid = data.get('uid')
        print('decoded_token', decoded_token)
        print('uid', uid)    
        try:     
            firebase_user = auth.get_user(uid)
            if firebase_user:
                FirebaseUser.objects.update_or_create(uid=uid, 
                                                    defaults={
                                                            'email': firebase_user.email,
                                                            'phone_number': firebase_user.phone_number,
                                                            'display_name': firebase_user.display_name,
                                                            'photo_url': firebase_user.photo_url,
                                                            'latest_token': token,
                                                            'latest_token_exp': decoded_token['exp'],
                                                        },
                                                        )
        except Exception as e:
            print('Error when using auth.get_user(): ', e)
            
        # Serialize the data
        session_data = json.dumps({'uid': uid, 'exp': exp})

        # Store in session
        # request.session['firebase_data'] = session_data
         # Use sync_to_async to set the session data
        await sync_to_async(request.session.__setitem__)('firebase_data', session_data)
        return JsonResponse({'success': True, 'message': 'Token verified successfully'}, status=200)


    # Return an error response if the request method is not POST
    return JsonResponse({'success': False, 'error': 'Method not allowed'})


