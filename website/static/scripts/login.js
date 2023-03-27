const sectionList = document.querySelectorAll("section");

const changeToAttendance = () => {
  for (i = 0; i < sectionList.length; ++i) {
    if (
      sectionList[i].id != "attendanceSection" &&
      sectionList[i].id != "navbarSection"
    )
      sectionList[i].style.display = "none";
    else sectionList[i].style.display = "block";
  }
  document.title = "Attendance | KIIT SAP";
};

const changeToLogin = () => {
  for (i = 0; i < sectionList.length; ++i) {
    if (sectionList[i].id != "loginSection")
      sectionList[i].style.display = "none";
    else sectionList[i].style.display = "block";
  }
  document.title = "Sign in | KIIT SAP";
};

document.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("userid") === null) {
    changeToLogin();
  } else {
    changeToAttendance();
  }
});

let submitLoginBtn = document.getElementById("submitLogin");
submitLoginBtn.addEventListener("click", (event) => {
  event.preventDefault();
  let userid = document.getElementById("floatingID");
  let password = document.getElementById("floatingPassword");

  // remove error message, disable and insert loading spinner in button
  document.getElementById("errMsg").innerHTML = "";
  submitLoginBtn.disabled = true;
  submitLoginBtn.innerHTML = `
    <span class="spinner-border spinner-border-sm" id="btnLoadingSpinner"></span> Loading`;

  let request_options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      userid: userid.value,
      password: password.value,
    }),
  };
  fetch("/check_id", request_options)
    .then((response) => response.text())
    .then((data) => {
      console.log(data);
      if (data == "True") {
        // switch to attendance section, and set credentials in localstorage for future use
        changeToAttendance();
        localStorage.setItem("userid", userid.value);
        localStorage.setItem("password", password.value);
      } else if (data == "False") {
        // Revert sign in button and display error message
        submitLoginBtn.disabled = false;
        submitLoginBtn.innerHTML = "Sign in";
        document.getElementById("errMsg").innerHTML =
          "Invalid User ID/Password, or SAP is unreachable";
      }
    })
    .catch((err) => console.log(err));
});


let LogoutBtn = document.getElementById("signout");
LogoutBtn.addEventListener("click", (event) => {
  event.preventDefault();
  localStorage.removeItem("userid");
  localStorage.removeItem("password");
  changeToLogin();
  submitLoginBtn.disabled = false;
  submitLoginBtn.innerHTML = "Sign in";
});
