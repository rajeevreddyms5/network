document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#followButton').addEventListener('onsubmit', () => load_follow('inbox', username));

});



// archive function
function archive_state(id, state) {
  if (state === false) {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
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
