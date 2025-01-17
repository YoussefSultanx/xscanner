// static/js/firebase-config.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyDfjcl7cWfEBVh6wSJSSb5BuY3nWd4_O50",
  authDomain: "web-vulnerability-scanne-4aba6.firebaseapp.com",
  projectId: "web-vulnerability-scanne-4aba6",
  storageBucket: "web-vulnerability-scanne-4aba6.appspot.com",
  messagingSenderId: "685311230238",
  appId: "1:685311230238:web:b7ba4f015361c8a1ec890f"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth();

document.getElementById('register-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    createUserWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Registered successfully
            window.location.href = '/login';
        })
        .catch((error) => {
            console.error(error);
        });
});

document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Logged in successfully
            window.location.href = '/home';
        })
        .catch((error) => {
            console.error(error);
        });
});
