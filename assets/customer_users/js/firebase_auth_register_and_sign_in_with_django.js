  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-analytics.js";
  // Add Firebase products that you want to use
  import { getAuth, signInWithPopup, signInWithEmailAndPassword, TwitterAuthProvider, GoogleAuthProvider, createUserWithEmailAndPassword} from 'https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js';
  import { RecaptchaVerifier, signInWithPhoneNumber} from 'https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js';
  import { isSignInWithEmailLink, signInWithEmailLink, sendSignInLinkToEmail } from "firebase/auth";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyAUKEAAmqwcJ3fI9JSMLMhprCRIT9YZ5_c",
    authDomain: "fresh-start-9fdb6.firebaseapp.com",
    projectId: "fresh-start-9fdb6",
    storageBucket: "fresh-start-9fdb6.appspot.com",
    messagingSenderId: "214895272406",
    appId: "1:214895272406:web:d82b1c8b656960960a0477",
    measurementId: "G-ZD73MVNY42"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
  // Initialize Firebase Authentication and get a reference to the service
  const firebase_auth = getAuth(app);


  $(document).ready(function() {
    $('#email-signup-button').click(function(e) {
      e.preventDefault();

      var email = $('#email').val();
      var password = $('#password').val();
      var display_name = $('#display-name').val();
      email = email.toLowerCase();
      display_name = display_name.split(' ')
        .map(word => word.replace(word[0], word[0].toUpperCase()))
        .join(' ');

      createUserWithEmailAndPassword(firebase_auth, email, password)
        .then((userCredential) => {
          // var user = firebase.auth().currentUser;
          var user = userCredential.user;
          user.display_name = display_name

          var userObj = {
          uid: user.uid,
          email: user.email,
          display_name: display_name,
          password: password,  // It's highly not recommended to send passwords
          };
          
          // serialize the data 
          var jsonUserObj = JSON.stringify(userObj)
          createFirebaseUserInDjango(jsonUserObj);
        })
        .catch((error) => {
          console.error(error);
        });
    });
    // end of email sign up button

    $('#google-signup-button').click(function(e) {
        e.preventDefault();
        var provider = new GoogleAuthProvider();
        signInWithPopup(firebase_auth, provider)
          .then((result) => {
            const credential = GoogleAuthProvider.credentialFromResult(result);
            const token = credential.accessToken;
            // The signed-in user info.
            const user = result.user;
      
            // Create a user object that we will send to Django
            var userObj = {
            uid: user.uid,
            email: user.email,
            display_name: user.displayName,
            token: token,
            credential:credential,
            };
    
            // Serialize the data in JSON
            var jsonUserObj = JSON.stringify(userObj);
    
            // Now send the data to Django
            $.ajax({
            url: 'sign_up_via_gmail_to_backend/',
            type: 'post',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            data: jsonUserObj,
            datatype: 'json',
            success: function(response) {
                if(response.status === 'OK') {
                    window.location.href = response.redirect;
                }
            },
            error: function(response) {
                console.error("Error sending user data to the backend", response);
            }
            });
            
            console.log('User signed up with Google!');
        })
        .catch((error) => {
        console.error(error);
        });
    });

    $('#twitter-signup-button').click(function(e) {
      e.preventDefault();
      var provider = new TwitterAuthProvider();
      signInWithPopup(firebase_auth, provider)
        .then((result) => {
          console.log('User signed up with Twitter!');
        })
        .catch((error) => {
          console.error(error);
        });
    });

    function createFirebaseUserInDjango(jsonUserObj) {
      // Get CSRF token
      var csrftoken = $('input[name=csrfmiddlewaretoken]').val();

      // Implement the logic to send user data to the backend server
      // You may send the user data via AJAX POST request
      $.ajax({
          url: 'firebase_auth_user_creation/',
          type: 'post',
          headers: {
                  'Content-Type': 'application/json',
                  // Add the CSRF token to the request header
                  'X-CSRFToken': csrftoken,
              },
          data: jsonUserObj,
          // {
          //     'uid': user.uid,
          //     'email': user.email,
          //     'display_name': user.display_name,
          //     'password':user.password,
          //     // other user attributes
          //     // Add CSRF Token
          //     'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
          // },
          datatype: 'json',
            beforeSend: function(xhr) {
              xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
          },
          success: function(data) {
            // alert(data.message);
            // Redirect to the URL provided by backend
            window.location.href = '/accounts/register-success/';
          },

          error: function(response) {
              console.error("Error sending user data to the backend (Django).", response);
          }
      });
      // end of ajax
    }
    // end of function 

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

  // Email & Password Authentication
  $('#email-login-button').click(function (e) {
      e.preventDefault();
      var email = $('#email').val();
      var password = $('#password').val();
      signInWithEmailAndPassword(firebase_auth, email, password)
          .then((userCredential) => {
              console.log('Signed in as ', email);
              $("#email-error").html("");
              // Signed in 
              const user = userCredential.user;
              firebaseAuthSigninPrecheck(user);
          })
          .catch((error) => {
              console.error('Error signing in with email and password', error);
              $("#email-error").html(error.message);
          });
    });

  
  // Phone Number Authentication
  window.recaptchaVerifier = new RecaptchaVerifier('sign-in-button', {
      'size': 'invisible',
      'callback': (response) => {
          onSignInSubmit();
      }
  },firebase_auth);


  function onSignInSubmit() {
      const phoneNumber = $('#phone').val();
      // const phoneNumber = getPhoneNumberFromUserInput();
      const appVerifier = window.recaptchaVerifier;

      
      signInWithPhoneNumber(firebase_auth, phoneNumber, appVerifier)
          .then((confirmationResult) => {
              window.confirmationResult = confirmationResult;
              const code = window.prompt("Enter the OTP sent to your phone");
              // const code = getCodeFromUserInput();
              confirmationResult.confirm(code).then((result) => {
                  console.log("User signed in");
                  $("#phone-error").html("");
                  const user = result.user;
              }).catch((error) => {
                  console.error("Error while checking the verification code", error);
                  $("#phone-error").html(error.message);
              });
          }).catch((error) => {
              console.error("Error while sending the SMS", error);
              $("#phone-error").html(error.message);
          });
    }
 

});
// end of document ready 

// Email & Password Authentication
$('#email-login-button').click(function (e) {
    e.preventDefault();
    var email = $('#email').val();
    var password = $('#password').val();
    signInWithEmailAndPassword(firebase_auth, email, password)
        .then((userCredential) => {
          console.log('Signed in as ', email);
          $("#email-error").html("");
          // Signed in 
          const user = userCredential.user;
          user.sendEmailVerification().then(function() {
            console.log("Verification email sent.");
          }).catch(function(error) {
              console.error("Error sending verification email.", error);
          });

          firebaseAuthSigninPrecheck(user);
        })
        .catch((error) => {
            console.error('Error signing in with email and password', error);
            $("#email-error").html(error.message);
        });
});


// Phone Number Authentication
window.recaptchaVerifier = new RecaptchaVerifier('sign-in-button', {
    'size': 'invisible',
    'callback': (response) => {
        onSignInSubmit();
    }
},firebase_auth);


function onSignInSubmit() {
    const phoneNumber = $('#phone').val();
    // const phoneNumber = getPhoneNumberFromUserInput();
    const appVerifier = window.recaptchaVerifier;

    
    signInWithPhoneNumber(firebase_auth, phoneNumber, appVerifier)
        .then((confirmationResult) => {
            window.confirmationResult = confirmationResult;
            const code = window.prompt("Enter the OTP sent to your phone");
            // const code = getCodeFromUserInput();
            confirmationResult.confirm(code).then((result) => {
                console.log("User signed in");
                $("#phone-error").html("");
                const user = result.user;
            }).catch((error) => {
                console.error("Error while checking the verification code", error);
                $("#phone-error").html(error.message);
            });
        }).catch((error) => {
            console.error("Error while sending the SMS", error);
            $("#phone-error").html(error.message);
        });
  }

function firebaseAuthSigninPrecheck(user) {
          // Implement the logic to send user data to the backend server
          // You may send the user data via AJAX POST request
        // Serialize the data in JSON
        var userObj = {
            'uid': user.uid,
            'email': user.email,
            // other user attributes
            // // Add CSRF Token
            // 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        };
        var jsonUserObj = JSON.stringify(userObj);
          $.ajax({
              url: 'firebase_auth_signin_precheck/',
              type: 'post',
              headers: {
                'Content-Type': 'application/json',
                // Add the CSRF token to the request header
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
            },
              data: jsonUserObj,
              datatype:'json',
              success: function(response) {
                  if(response.redirect_url) {
                      window.location.href = response.redirect_url;
                  }
              },
              error: function(response) {
                  console.error("Error sending user data to the backend", response);
              }
          });
      }
