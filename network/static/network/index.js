document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#edit").addEventListener("click", edit);
    document.querySelector("#like").addEventListener("click", like)
    document.querySelector("#unlike").addEventListener("click", unlike)
});

function edit() {
    const id = this.dataset.id;
    const url = this.dataset.url;
    const el1 = document.createElement('input');
    const el2 = document.createElement('textarea');
    el1.type = "text";
    el1.name = "subject";
    el1.value = document.getElementById(id).querySelector('#subject').innerHTML;
    el2.name = "body";
    el2.value = document.getElementById(id).querySelector('#body').innerHTML;
    const button = document.createElement('input')
    button.type = "submit";
    button.value = "Save";
    button.dataset.id = id;
    button.addEventListener("click", () => {
        const subject = el1.value;
        const body = el2.value;
        const num = this.dataset.id;
        fetch('/edit', {
            method: 'POST',
            body: JSON.stringify({
              subject: subject,
              body: body,
              num: num
            })
          })
          .then(response => {
            console.log(response);
            window.location.href = url;
    })
    .catch(error => {
         
        console.log(error);
      });
    })    
    document.getElementById(id).innerHTML = "";
    document.getElementById(id).append(el1);
    document.getElementById(id).append("  ");
    document.getElementById(id).append(el2);
    document.getElementById(id).append("  ");
    document.getElementById(id).append(button);
}

function like() {
  const id = this.dataset.id;
  const url = this.dataset.url;
  fetch('/likes', {
    method: 'POST',
    body: JSON.stringify({
      task: "like",
      id: id
    })
  })
  .then(response => {
    console.log(response);
    window.location.href = url;
})
.catch(error => {
 
console.log(error);
});
}

function unlike() {
  const id = this.dataset.id;
  const url = this.dataset.url;
  fetch('/likes', {
    method: 'POST',
    body: JSON.stringify({
      task: "unlike",
      id: id
    })
  })
  .then(response => {
    console.log(response);
    window.location.href = url;
})
.catch(error => {
 
console.log(error);
});
}