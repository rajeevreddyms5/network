

document.addEventListener('DOMContentLoaded', function() {

  // select all ids of likeButton and for each click on likeButton load_likes function
  document.querySelectorAll('#likeButton').forEach(function(element) {
    element.addEventListener('click', load_likes);
  })

  // on window reload remove local storage and set editForm method to post
  window.onload = function() {
    localStorage.removeItem('editID');
    localStorage.removeItem('divID');
    document.querySelector('#editForm').setAttribute('method', 'post');
    document.querySelector("#postButton").setAttribute('type', 'submit');
  }

  // select the id of post button and on click call the savePost function
  //if (localStorage.getItem('editID') !== null) {
  //  document.querySelector('#postButton').addEventListener('click', savePost);
  //}

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

    // select the form element with id editForm
    var divID = this.event.target.id;
    result = divID.slice(9, divID.length); // get the number of the div
    console.log(result);

    // set the number to local storage
    localStorage.setItem('divID', result);

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

          // select the post button and change its type to button
          document.querySelector("#postButton").setAttribute('type', 'button');
      });
    
    // Stop form from submitting
    return false

  }

  // function to get csrf token
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

  // function to save the edited post
  function savePost(event) {

    // get the divID from local storage
    var divID = localStorage.getItem('divID');
    console.log(divID);

    // select the div element with id divID{result}
    var div = document.getElementById(`postContent${result}`);
    console.log(div);

    // get post id
    post_id = Number(localStorage.getItem('editID'));

    // get csrf token from id editForm and set it to token
    var csrftoken = getCookie('csrftoken');
    console.log(csrftoken);


    const request = new Request(
      `/posts/${post_id}`,
      {
          method: 'PUT',
          headers: {'X-CSRFToken': csrftoken},
          mode: 'same-origin', // Do not send CSRF token to another domain.
          body: JSON.stringify({
            csrfmiddlewaretoken: csrftoken,
            content: document.querySelector('#exampleFormControlTextarea1').value
          }),
      }
    );

    fetch(request).then(function(response) {
      // ...
    });

    // change the inner html text of the div to value of the exampleformcontroltextarea1
    div.innerHTML = document.querySelector('#exampleFormControlTextarea1').value

    // clear textarea
    document.querySelector('#exampleFormControlTextarea1').value = '';


    // Stop form from submitting
    return false

  }