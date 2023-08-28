document.addEventListener('DOMContentLoaded', function() {

  // select all ids of likeButton and for each click on likeButton load_likes function
  document.querySelectorAll('#likeButton').forEach(function(element) {
    element.addEventListener('click', load_likes);
  })

  
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
  function editPost(id) {

    // select the class "form-group" and populate the fields with the data from the post the user wants to edit
    alert("you clicked the edit button of " + id);


  }