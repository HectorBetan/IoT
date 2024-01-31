// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
//import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDG1Rcm7-Z2GKwf9m3k5CW2VhUs2JWxxXo",
  authDomain: "eco-sistema-iot.firebaseapp.com",
  projectId: "eco-sistema-iot",
  storageBucket: "eco-sistema-iot.appspot.com",
  messagingSenderId: "473106983632",
  appId: "1:473106983632:web:d8500625c4bc6cd7e80cd5",
  measurementId: "G-S0D8QJN7GP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
//const analytics = getAnalytics(app);
export const db = getFirestore(app);