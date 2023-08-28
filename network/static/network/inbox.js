

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
  function editPost(post_id) {

    // fetch the post using API
    fetch(`/posts/${post_id}`)
      .then(response => response.json())
      .then(post => {
          // Print email
          console.log(post);

          // ... do something else with post ...
          

      }); 
    
  }