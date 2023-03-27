const insertSpinner = () => {
  document.getElementById("attendanceRow").innerHTML = `
    <div class="text-center" id="spinner" style="margin: 5rem auto;">
      <div class="spinner-border text-light" style="width: 5rem; height: 5rem;"></div>
      <h5 class="text-light">Fetching your attendance...</h5>
    </div>`;
};

const getPregressBarColor = (percent) => {
  if (parseFloat(percent) >= 75) return "bg-success";
  else if (parseFloat(percent) < 65) return "bg-danger";
  else return "bg-warning";
};

const insertAttendance = (attendance) => {
  let attendanceRow = document.getElementById("attendanceRow");
  for (let i = 0; i < attendance["Subject"].length; i++) {
    attendanceRow.innerHTML += `
      <div class="col mb-3">
        <div class="card attendance-card">
          <div style="height: 5rem;">
            <h5 class="card-title text-light mx-2 my-1">
              ${attendance["Subject"][i]}
            </h5>
            <p class="card-text text-light mx-2 my-0">
              ${attendance["Faculty Name"][i]}
            </p>
            </div>
            <p class="card-text text-light mx-2 my-0 text-end">
              ${attendance["Total Percentage"][i].slice(0, -1)}% | ${attendance[
      "No. of Present"
    ][i].slice(0, -3)}/${attendance["No. of Days"][i].slice(0, -3)}
            </p>
          <div
            class="progress"
            style="height: 1.5rem; border-radius: 0 0 0.5rem 0.5rem"
          >
            <div
              class="progress-bar ${getPregressBarColor(
                attendance["Total Percentage"][i]
              )}"
              style="width: ${attendance["Total Percentage"][i]}%"
            ></div>
          </div>
        </div>
      </div>`;
  }
};

const submitAttendanceBtn = document.getElementById("submitAttendance");
submitAttendanceBtn.addEventListener("click", (event) => {
  event.preventDefault();
  let userid = localStorage.getItem("userid");
  let password = localStorage.getItem("password");
  let year = document.getElementById("year").value;
  let session = document.getElementById("session").value;

  // disable and insert loading spinner in button
  submitAttendanceBtn.disabled = true;
  submitAttendanceBtn.innerHTML = `
    <span class="spinner-border spinner-border-sm" id="btnLoadingSpinner"></span> Loading`;

  //clear attendance content and insert spinner until real attendance loaded
  insertSpinner();

  let request_options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      userid: userid,
      password: password,
      year: year,
      session: session,
    }),
  };
  fetch("get_attendance", request_options)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      insertAttendance(data);
      document.getElementById("spinner").remove();
    })
    .catch((err) => console.log(err));
  
  //revert submit button after attendance successfully shown
  submitAttendanceBtn.disabled = false;
  submitAttendanceBtn.innerHTML = "Get Attendance";
});
