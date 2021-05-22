window.onload = () => {
    updateToken = document.getElementById('updateToken')
    updateToken.addEventListener('click', updateTokenAction);


    getData = document.getElementById('getData')
    getData.addEventListener('click', getWigetData);
    
}

function uuid4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
  }

async function setValueById(id, value){
    e = document.getElementById(id)
    e.value = value
}

