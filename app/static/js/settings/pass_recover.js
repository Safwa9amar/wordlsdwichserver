document.addEventListener('DOMContentLoaded', ()=>{

}
)


function recoverPassword(event, $w) {
    // Change all values to your own
    let params = {
        user_id: 'fAA9vgLJK9IaNRTSG',
        service_id: 'service_rxn0bar',
        template_id: 'template_2wkfycf',
        template_params: {
          'to_name': 'YOUR_PARAM1_VALUE',
          'lien': 'YOUR_PARAM2_VALUE'
        }
    };
  
    let headers = {
        'Content-type': 'application/json'
    };
  
    let options = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(params)
    };
  
    fetch('https://api.emailjs.com/api/v1.0/email/send', options)
      .then((httpResponse) => {
          if (httpResponse.ok) {
              console.log('Your mail is sent!');
          } else {
              return httpResponse.text()
                .then(text => Promise.reject(text));
          }
      })
      .catch((error) => {
          console.log('Oops... ' + error);
      });
  }