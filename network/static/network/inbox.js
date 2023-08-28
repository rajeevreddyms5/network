

document.addEventListener('DOMContentLoaded', function() {

  // select all ids of likeButton and for each click on likeButton load_likes function
  document.querySelectorAll('#likeButton').forEach(function(element) {
    element.addEventListener('click', load_likes);
  })

  // on window reload remove local storage and set editForm method to post
  window.onload = function() {
    localStorage.removeItem('editID')
    document.querySelector('#editForm').setAttribute('method', 'post');
  }

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
          textarea = document.querySelector('#exampleFormControlTextarea1');
          textarea.focus();
          textarea.value = post.content;

          // post value to post button
          localStorage.setItem('editID', post_id)

          // select the form element with id editForm and change its method to PUT
          document.querySelector('#editForm').setAttribute('method', 'PUT');

          
      });
    
    // Stop form from submitting
    return false
    
  }


  // function to save the edited post
  function savePost() {
    // get post id
    id = Number(localStorage.getItem('editID'));

    // send to console
    console.log(id);

    // Stop form from submitting
    return false

  }