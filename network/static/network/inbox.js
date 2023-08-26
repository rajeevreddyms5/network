document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#likeButton').addEventListener('click', () => load_likes());
  document.querySelectorAllbyclassName('page-link').forEach((element) => {
    element.addEventListener('click', () => load_view(());
  });

});


// like and unlike function
function load_likes() {

  alert("you clicked the like button");

  if (state === false) {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        user_name: true
      })
    });
    load_mailbox('inbox');
  }
  else {
    fetch(`/emails/${id}`, { 
      method: 'PUT', 
      body: JSON.stringify({ 
        archived: false 
      }) 
    });
    load_mailbox('inbox');
  }

  // refresh webpage
  location.reload();
}



// create view function where javascript changes class name to active
function load_view() {

  // alert to test button
  alert("test");

  // remove active class from nav tabs
  nav_div = document.getElementById("home-tab");
  nav_div.classList.remove("active");

  // add active class to nav tabs
  nav_div = document.getElementById("profile-tab");
  nav_div.classList.add("active");

  //
  document.getElementById("profile-tab-pane").className = "tab-pane fade show active";
  document.getElementById("home-tab-pane").className = "tab-pane fade";
}