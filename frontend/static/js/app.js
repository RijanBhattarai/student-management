/* ================================================================
   Student Management System — Frontend JavaScript
   Author : Rijan
   Notes  : Communicates with Flask REST API via fetch()
================================================================ */

const API = "";   // Same origin — Flask serves both front and back

// ── Page navigation ─────────────────────────────────────────
document.querySelectorAll(".nav-link").forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    const page = link.dataset.page;
    // Update active nav
    document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
    link.classList.add("active");
    // Show correct page
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.getElementById(`page-${page}`).classList.add("active");
    // Update title
    document.getElementById("page-title").textContent =
      { dashboard:"Dashboard", students:"Students", courses:"Courses", enrollments:"Enrollments" }[page];
    // Load data for page
    if (page === "dashboard")   loadDashboard();
    if (page === "students")    loadStudents();
    if (page === "courses")     loadCourses();
    if (page === "enrollments") loadEnrollmentPage();
  });
});

// Show current date in topbar
document.getElementById("current-date").textContent =
  new Date().toLocaleDateString("en-US", { weekday:"short", year:"numeric", month:"short", day:"numeric" });

// ── Toast notification ───────────────────────────────────────
function showToast(msg, type = "success") {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className   = `toast ${type}`;
  setTimeout(() => t.classList.add("hidden"), 3000);
}

// ── Modal helpers ────────────────────────────────────────────
function closeModal(id) { document.getElementById(id).classList.add("hidden"); }
function openModal(id)  { document.getElementById(id).classList.remove("hidden"); }

// Close modal on backdrop click
document.querySelectorAll(".modal-overlay").forEach(overlay => {
  overlay.addEventListener("click", e => {
    if (e.target === overlay) overlay.classList.add("hidden");
  });
});


/* ════════════════════════════════════════════════════════════
   DASHBOARD
════════════════════════════════════════════════════════════ */
async function loadDashboard() {
  const res  = await fetch(`${API}/api/stats`);
  const data = await res.json();

  document.getElementById("stat-total").textContent   = data.total_students;
  document.getElementById("stat-active").textContent  = data.active_students;
  document.getElementById("stat-courses").textContent = data.total_courses;
  document.getElementById("stat-gpa").textContent     = data.avg_gpa.toFixed(2);

  // Program chart
  const maxP = Math.max(...data.by_program.map(p => p.count));
  document.getElementById("program-chart").innerHTML = data.by_program.map(p => `
    <div class="bar-row">
      <span class="bar-label" title="${p.program}">${p.program.replace("BSc ","")}</span>
      <div class="bar-fill-wrap">
        <div class="bar-fill" style="width:${(p.count/maxP*100)}%"></div>
      </div>
      <span class="bar-val">${p.count}</span>
    </div>`).join("");

  // Year chart
  const maxY = Math.max(...data.by_year.map(y => y.count));
  document.getElementById("year-chart").innerHTML = data.by_year.map(y => `
    <div class="bar-row">
      <span class="bar-label">Year ${y.year}</span>
      <div class="bar-fill-wrap">
        <div class="bar-fill" style="width:${(y.count/maxY*100)}%;background:#2A9D8F"></div>
      </div>
      <span class="bar-val">${y.count}</span>
    </div>`).join("");
}


/* ════════════════════════════════════════════════════════════
   STUDENTS
════════════════════════════════════════════════════════════ */
async function loadStudents() {
  const search  = document.getElementById("search-input").value;
  const program = document.getElementById("filter-program").value;
  const status  = document.getElementById("filter-status").value;

  const params = new URLSearchParams();
  if (search)  params.set("search",  search);
  if (program) params.set("program", program);
  if (status)  params.set("status",  status);

  const res  = await fetch(`${API}/api/students?${params}`);
  const rows = await res.json();
  const tbody = document.getElementById("students-tbody");

  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="8" class="empty-state">No students found.</td></tr>`;
    return;
  }

  tbody.innerHTML = rows.map((s, i) => {
    const gpaClass = s.gpa >= 3.5 ? "gpa-high" : s.gpa >= 2.5 ? "gpa-mid" : "gpa-low";
    const badge    = s.status === "Active" ? "badge-active" : "badge-inactive";
    return `
      <tr>
        <td>${i+1}</td>
        <td><strong>${s.full_name}</strong></td>
        <td>${s.email}</td>
        <td style="max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${s.program}</td>
        <td>Year ${s.year}</td>
        <td class="${gpaClass}">${s.gpa.toFixed(2)}</td>
        <td><span class="badge ${badge}">${s.status}</span></td>
        <td><div class="actions">
          <button class="btn btn-sm btn-edit" onclick="editStudent(${s.id})"><i class="fas fa-edit"></i></button>
          <button class="btn btn-sm btn-del"  onclick="confirmDelete('student',${s.id},'${s.full_name}')"><i class="fas fa-trash"></i></button>
        </div></td>
      </tr>`;
  }).join("");
}

// Live search & filter
document.getElementById("search-input").addEventListener("input", loadStudents);
document.getElementById("filter-program").addEventListener("change", loadStudents);
document.getElementById("filter-status").addEventListener("change", loadStudents);

// Open blank add-student modal
function openStudentModal() {
  document.getElementById("student-modal-title").textContent = "Add Student";
  ["s-id","s-name","s-email","s-phone","s-dob","s-address","s-gpa"].forEach(id =>
    document.getElementById(id).value = "");
  document.getElementById("s-gender").value  = "";
  document.getElementById("s-program").value = "";
  document.getElementById("s-year").value    = "1";
  document.getElementById("s-status").value  = "Active";
  openModal("student-modal");
}

// Populate modal for editing
async function editStudent(id) {
  const res = await fetch(`${API}/api/students/${id}`);
  const s   = await res.json();
  document.getElementById("student-modal-title").textContent = "Edit Student";
  document.getElementById("s-id").value      = s.id;
  document.getElementById("s-name").value    = s.full_name;
  document.getElementById("s-email").value   = s.email;
  document.getElementById("s-phone").value   = s.phone   || "";
  document.getElementById("s-dob").value     = s.dob     || "";
  document.getElementById("s-gender").value  = s.gender  || "";
  document.getElementById("s-address").value = s.address || "";
  document.getElementById("s-program").value = s.program;
  document.getElementById("s-year").value    = s.year;
  document.getElementById("s-gpa").value     = s.gpa;
  document.getElementById("s-status").value  = s.status;
  openModal("student-modal");
}

// Save (add or update)
async function saveStudent() {
  const id = document.getElementById("s-id").value;
  const body = {
    full_name: document.getElementById("s-name").value.trim(),
    email:     document.getElementById("s-email").value.trim(),
    phone:     document.getElementById("s-phone").value.trim(),
    dob:       document.getElementById("s-dob").value,
    gender:    document.getElementById("s-gender").value,
    address:   document.getElementById("s-address").value.trim(),
    program:   document.getElementById("s-program").value,
    year:      document.getElementById("s-year").value,
    gpa:       document.getElementById("s-gpa").value || 0,
    status:    document.getElementById("s-status").value,
  };

  if (!body.full_name || !body.email || !body.program) {
    showToast("Please fill in all required fields.", "error");
    return;
  }

  const url    = id ? `${API}/api/students/${id}` : `${API}/api/students`;
  const method = id ? "PUT" : "POST";

  const res  = await fetch(url, { method, headers:{"Content-Type":"application/json"}, body: JSON.stringify(body) });
  const data = await res.json();

  if (!res.ok) { showToast(data.error || "Error saving student.", "error"); return; }
  closeModal("student-modal");
  showToast(id ? "Student updated successfully!" : "Student added successfully!");
  loadStudents();
  loadDashboard();
}


/* ════════════════════════════════════════════════════════════
   COURSES
════════════════════════════════════════════════════════════ */
async function loadCourses() {
  const res   = await fetch(`${API}/api/courses`);
  const rows  = await res.json();
  const tbody = document.getElementById("courses-tbody");

  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state">No courses found.</td></tr>`;
    return;
  }
  tbody.innerHTML = rows.map(c => `
    <tr>
      <td><strong>${c.code}</strong></td>
      <td>${c.name}</td>
      <td>${c.credits} cr</td>
      <td>${c.instructor || "—"}</td>
      <td>${c.semester  || "—"}</td>
      <td><div class="actions">
        <button class="btn btn-sm btn-del" onclick="confirmDelete('course',${c.id},'${c.name}')">
          <i class="fas fa-trash"></i>
        </button>
      </div></td>
    </tr>`).join("");
}

function openCourseModal() {
  ["c-code","c-name","c-instructor","c-semester"].forEach(id =>
    document.getElementById(id).value = "");
  document.getElementById("c-credits").value = "3";
  openModal("course-modal");
}

async function saveCourse() {
  const body = {
    code:       document.getElementById("c-code").value.trim(),
    name:       document.getElementById("c-name").value.trim(),
    credits:    document.getElementById("c-credits").value,
    instructor: document.getElementById("c-instructor").value.trim(),
    semester:   document.getElementById("c-semester").value.trim(),
  };
  if (!body.code || !body.name) { showToast("Code and Name are required.", "error"); return; }

  const res  = await fetch(`${API}/api/courses`, {
    method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) { showToast(data.error || "Error adding course.", "error"); return; }
  closeModal("course-modal");
  showToast("Course added successfully!");
  loadCourses();
  loadDashboard();
}


/* ════════════════════════════════════════════════════════════
   ENROLLMENTS
════════════════════════════════════════════════════════════ */
async function loadEnrollmentPage() {
  // Populate student dropdown
  const res  = await fetch(`${API}/api/students`);
  const list = await res.json();
  const sel  = document.getElementById("enroll-student-select");
  sel.innerHTML = `<option value="">-- Choose a student --</option>` +
    list.map(s => `<option value="${s.id}">${s.full_name}</option>`).join("");
}

async function loadEnrollments() {
  const sid   = document.getElementById("enroll-student-select").value;
  const tbody = document.getElementById("enrollments-tbody");
  if (!sid) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state">Select a student above</td></tr>`;
    return;
  }
  const res  = await fetch(`${API}/api/students/${sid}/enrollments`);
  const rows = await res.json();
  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state">No enrollments found for this student.</td></tr>`;
    return;
  }
  tbody.innerHTML = rows.map(e => `
    <tr>
      <td><strong>${e.code}</strong></td>
      <td>${e.name}</td>
      <td>${e.credits} cr</td>
      <td>${e.semester || "—"}</td>
      <td><span class="badge badge-grade">${e.grade}</span></td>
      <td>
        <button class="btn btn-sm btn-del" onclick="removeEnrollment(${e.id})">
          <i class="fas fa-times"></i> Remove
        </button>
      </td>
    </tr>`).join("");
}

async function openEnrollModal() {
  // Populate dropdowns
  const [sRes, cRes] = await Promise.all([
    fetch(`${API}/api/students`),
    fetch(`${API}/api/courses`)
  ]);
  const students = await sRes.json();
  const courses  = await cRes.json();

  document.getElementById("e-student").innerHTML =
    students.map(s => `<option value="${s.id}">${s.full_name}</option>`).join("");
  document.getElementById("e-course").innerHTML =
    courses.map(c => `<option value="${c.id}">${c.code} — ${c.name}</option>`).join("");

  openModal("enroll-modal");
}

async function saveEnrollment() {
  const body = {
    student_id: parseInt(document.getElementById("e-student").value),
    course_id:  parseInt(document.getElementById("e-course").value),
    grade:      document.getElementById("e-grade").value,
  };
  const res  = await fetch(`${API}/api/enrollments`, {
    method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(body)
  });
  const data = await res.json();
  if (!res.ok) { showToast(data.error || "Enrollment failed.", "error"); return; }
  closeModal("enroll-modal");
  showToast("Student enrolled successfully!");
  loadEnrollments();
}

async function removeEnrollment(eid) {
  await fetch(`${API}/api/enrollments/${eid}`, { method:"DELETE" });
  showToast("Enrollment removed.");
  loadEnrollments();
}


/* ════════════════════════════════════════════════════════════
   CONFIRM DELETE
════════════════════════════════════════════════════════════ */
function confirmDelete(type, id, name) {
  document.getElementById("confirm-msg").textContent =
    `Are you sure you want to delete ${type} "${name}"? This cannot be undone.`;
  const btn = document.getElementById("confirm-action-btn");
  btn.onclick = async () => {
    const url = type === "student" ? `${API}/api/students/${id}` : `${API}/api/courses/${id}`;
    await fetch(url, { method:"DELETE" });
    closeModal("confirm-modal");
    showToast(`${type.charAt(0).toUpperCase()+type.slice(1)} deleted.`);
    if (type === "student") { loadStudents(); loadDashboard(); }
    else { loadCourses(); loadDashboard(); }
  };
  openModal("confirm-modal");
}


// ── Load dashboard on initial page load ─────────────────────
loadDashboard();
