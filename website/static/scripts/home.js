const insertSpinner = () => {
  document.body.innerHTML += `
    <div class="text-center" id="spinner" style="margin-top: 5rem;">
      <div class="spinner-border" style="width: 5rem; height: 5rem;"></div>
      <h5>Fetching your attendance...</h5>
    </div>`;
};


const getPregressBarColor = (percent) => {
  if (parseFloat(percent) >= 75) return "bg-success";
  else if (parseFloat(percent) < 65) return "bg-danger";
  else return "bg-warning";
}


const insertAttendance = (attendance) => {
  const attendanceRow = document.getElementById("attendanceRow")
  for (let i = 0; i < attendance["Subject"].length; i++) {
    attendanceRow.innerHTML += `
      <div class="col mb-3">
        <div class="card">
          <div style="height: 5rem;">
            <h5 class="card-title mx-2 my-1">
              ${attendance["Subject"][i]}
            </h5>
            <p class="card-text mx-2 my-0">
              ${attendance["Faculty Name"][i]}
            </p>
            </div>
            <p class="card-text mx-2 my-0 text-end">
              ${attendance["Total Percentage"][i].slice(0, -1)}% | ${attendance["No. of Present"][i].slice(0, -3)}/${attendance["No. of Days"][i].slice(0, -3)}
            </p>
          <div
            class="progress"
            style="height: 1.5rem; border-radius: 0 0 0.5rem 0.5rem"
          >
            <div
              class="progress-bar ${getPregressBarColor(attendance["Total Percentage"][i])}"
              style="width: ${attendance["Total Percentage"][i]}%"
            ></div>
          </div>
        </div>
      </div>`
  }
}