
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import {  OBJLoader } from 'three/addons/loaders/OBJLoader.js';

//  0xeaedee 0xfffff0
// const geometry = new THREE.BoxGeometry( 0.5, 0.5, 0.5);
const material = new THREE.MeshBasicMaterial( { color: 0x049ef4 } );
const material2 = new THREE.MeshBasicMaterial( { color: 0x2C3E50 } );  //dark dark red

// this is the MeshStandardMaterial)()
var material3 = new THREE.MeshStandardMaterial();
material3.vertexColors = THREE.VertexColors;

// this is the MeshLambertMaterial
// Create a new MeshLambertMaterial
const material4 = new THREE.MeshLambertMaterial({ color: 0x049ef4, fog:true,  reflectivity:1,});
material4.reflectivity = 1;
material4.fog = true;

var scene1 = new THREE.Scene();
var scene2 = new THREE.Scene();
// scene1.fog = new THREE.Fog( 0x3f7b9d, 10, 15 );

var camera1 = new THREE.PerspectiveCamera(20, window.innerWidth / window.innerHeight, 0.5, 50);
// Set camera 1 position 
camera1.position.set(100, 100, 100);
camera1.updateProjectionMatrix(); // Update the camera's projection matrix
const depthTexture = new THREE.DepthTexture();
const depthMaterial = new THREE.MeshDepthMaterial({
  depthPacking: THREE.RGBADepthPacking, // Use RGBA packing for depth values
  alphaTest: 0.8 // Set an alpha threshold for depth testing
});

// adding the lights to the scene
const light = new THREE.AmbientLight( 0x3f7b9d ); // soft white light 0x404040
scene1.add( light );  
scene2.add( light );  

// Path to the first model
// const modelPath1 = './V8_Engine_V3.glb';
const modelPath1 = "{% static 'we_create_3d_models/3d_models/V8_Engine_V3.glb' %}"

// Path to the second model
// const modelPath2 = './Ignition.obj';
const modelPath2 = "{% static 'we_create_3d_models/3d_models/Ignition.obj' %}"

// const cube = new THREE.Mesh( geometry, material );
// scene.add( cube );

// Load and render the first model
const model1Container = document.getElementById('model1-convas-container');
const renderer1 = new THREE.WebGLRenderer();
renderer1.setSize(model1Container.clientWidth, model1Container.clientHeight);
// Assign the depth texture to the renderer's depthTexture property:
renderer1.depthTexture = depthTexture;
// Set the background color to light grey
renderer1.setClearColor(0xeaedee); // Use hexadecimal color code 
renderer1.autoClearDepth = true;
model1Container.appendChild(renderer1.domElement);

// Add controls
var controls1 = new OrbitControls(camera1, renderer1.domElement);
// controls.target.set(0, 0, 0); // Set the target position of the controls
// controls.autoRotate = true; // Enable auto-rotation

// Load and display the car engine model 1 via GLTFLoader(); gltf is web browser compatiblity
const loader1 = new GLTFLoader();
loader1.load(modelPath1, function (gltf) {
  var model = gltf.scene;
  model.traverse(function (child) {
  if (child instanceof THREE.Mesh) {

    // Assign the material to the mesh
    child.material = material4;
  }
  });
  scene1.add(model);
  // Set desired position, rotation, and scale of the model
  
  // Render the scene
  // renderer.render(scene, camera);

});

// Load and display the car engine model
// const loader2 = new FBXLoader() ;

// loader2.load("{% static 'we_create_3d_models/Ignition.fbx' %}", function (model) {

//     // Set desired position, rotation, and scale of the model
//     scene.add(model);
//     // Render the scene
//     // renderer.render(scene, camera);
    
// });

// Load the OBJ model
// const loader3 = new OBJLoader();
// // loader3.setMaterials( material2 );
// loader3.load("{% static 'we_create_3d_models/Ignition.obj' %}", function (model) {
//   // Set 
//   var center = new THREE.Vector3(); // Calculate the center of the model's bounding box
//   var boundingBox = new THREE.Box3().setFromObject(model); // Replace 'model' with your actual model variable
//   center = boundingBox.getCenter(center); // Get the center of the bounding box
//   model.position.sub( center ); // center the model
//   // obj.rotation.y = Math.PI;   // rotate the model
//   model.scale.set(1, 1, 1);
//   // model.traverse(function (child) {
//   model.traverse((child) => {  
//     if (child.isMesh ) { //child instanceof THREE.Mesh
//       child.material = material4; // material4; // material1;depthMaterial
//     }
//   });
//   scene.add(model);
//     // renderer.render(scene, camera);
// },
// // called when loading is in progresses
// function ( xhr ) {
//   console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
// },
// // called when loading has errors
// function ( error ) {
//   console.log( 'An error happened.' );
// }
// );

// Load and render the second model
const model2Container = document.getElementById('model2-convas-container');
const renderer2 = new THREE.WebGLRenderer();
renderer2.setSize(model2Container.clientWidth, model2Container.clientHeight);
model2Container.appendChild(renderer2.domElement);

scene2.fog = new THREE.Fog( 0x3f7b9d, 10, 15 );
var camera2 = new THREE.PerspectiveCamera(10, window.innerWidth / window.innerHeight, 0.5, 5000);

// Set camera position
camera2.position.set(1300, 1500, 1500);
camera2.updateProjectionMatrix(); // Update the camera's projection matrix

// Add controls 2
var controls2 = new OrbitControls(camera2, renderer2.domElement);
controls2.autoRotate = false;

// Load the second model (model 2) via OBJLoader loader
const loader2 = new OBJLoader();
// loader3.setMaterials( material2 );
loader2.load(modelPath2, function (model) {
  // Set 
  var center = new THREE.Vector3(); // Calculate the center of the model's bounding box
  var boundingBox = new THREE.Box3().setFromObject(model); // Replace 'model' with your actual model variable
  center = boundingBox.getCenter(center); // Get the center of the bounding box
  model.position.sub( center ); // center the model
  // obj.rotation.y = Math.PI;   // rotate the model
  model.scale.set(1, 1, 1);
  // model.traverse(function (child) {
  model.traverse((child) => {  
    if (child.isMesh ) { //child instanceof THREE.Mesh
      child.material = material4; // material4; // material1;depthMaterial
    }
  });
  scene2.add(model);
    // renderer.render(scene, camera);
},
// called when loading is in progresses
function ( xhr ) {
  console.log( ( xhr.loaded / xhr.total * 100 ) + '% loaded' );
},
// called when loading has errors
function ( error ) {
  console.log( 'An error happened.' );
}
);


// // Render the scene
function animate() {
    requestAnimationFrame(animate);
    // cube.rotation.x += 0.01;
    // cube.rotation.y += 0.01;
    // rotation.y += 0.01; // rotationSpeed;
    if (isAutoRotating) {
      controls1.autoRotate = true; // - controls.autoRotate;
      controls2.autoRotate = true; // - controls.autoRotate;
    }
    else {
        controls1.autoRotate = false;
        controls2.autoRotate = false;
    }
  
    renderer1.render(scene1, camera1);
    renderer2.render(scene2, camera2);
    controls1.update(); // Update the controls 1
    controls2.update(); // Update the controls 2
  }
  animate();
  