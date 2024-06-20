var firebaseConfig = {
    apiKey: "AIzaSyDsyFTYrxJ4KOGEkGZ7ZZiJzIigvqhULMU",
    authDomain: "wishstack-db.firebaseapp.com",
    databaseURL: "https://wishstack-db-default-rtdb.firebaseio.com",
    projectId: "wishstack-db",
    storageBucket: "wishstack-db.appspot.com",
    messagingSenderId: "809425693364",
    appId: "1:809425693364:web:908ca30fc4f9f6194485e1",
    measurementId: "G-T0FJ57Y7CY"
  };
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  var database = firebase.database()
  function save(){
    var email = document.getElementById('email').value
    var password = document.getElementById('pass').value
    var firstname = document.getElementById('fname').value
    var lastname = document.getElementById('lname').value
  database.ref('users/').set()({
    email:email,
    password:password,
    firstname:firstname,
    lastname:lastname
  })
  alert('save')
}