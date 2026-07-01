const form = document.querySelector("form");
form.addEventListener("submit",()=>{
    const button=document.querySelector("button");
    button.innerHTML="⏳ Organizing...";
    button.disabled=true;
});