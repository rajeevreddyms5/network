document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#likeButton').addEventListener('click', () => load_likes());

  // edit each post from posts
  document.querySelectorAll('#edit_post').forEach(edit => {
    edit.addEventListener('click', () => {
      alert("You clicked the edit button");
    });
  });
  

})


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


  // edit function to edit the post from posts
  function editPost() {

    // test
    alert("you clicked the edit button");

  }