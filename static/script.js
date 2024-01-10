function saveSelectionToLocalStorage(selectName, selectedValue) {
    localStorage.setItem(selectName, selectedValue);
}

function getSelectionFromLocalStorage(selectName) {
    return localStorage.getItem(selectName);
}

document.addEventListener('DOMContentLoaded', function () {
    const gradeSelect = document.querySelector('select[name="grade"]');
    const departmentSelect = document.querySelector('select[name="department"]');
    const halfPeriodSelect = document.querySelector('select[name="halfPeriod"]');
    const timetableTable = document.querySelector('table');

    gradeSelect.addEventListener('change', updateTimetable);
    departmentSelect.addEventListener('change', updateTimetable);
    halfPeriodSelect.addEventListener('change', updateTimetable);

    const savedGrade = getSelectionFromLocalStorage('grade');
    const savedDepartment = getSelectionFromLocalStorage('department');
    const savedHalfPeriod = getSelectionFromLocalStorage('halfPeriod');

    if (savedGrade) {
        gradeSelect.value = savedGrade;
    }

    if (savedDepartment) {
        departmentSelect.value = savedDepartment;
    }

    if (savedHalfPeriod) {
        halfPeriodSelect.value = savedHalfPeriod;
    }

    updateTimetable();

    async function updateTimetable() {
        const grade = gradeSelect.value;
        const department = departmentSelect.value;
        const halfPeriod = halfPeriodSelect.value;
        console.log(grade + "" + department + "" + halfPeriod);
    
        clearTimetable();
    
        const response = await fetch('/get_courses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `grade=${grade}&department=${department}&halfPeriod=${halfPeriod}`,
        });
    
        if (response.ok) {
            const responseData = await response.json();
    
            displayCourses(responseData.courses);
        } else {
            console.error('Failed to fetch courses');
        }
    }

    function clearTimetable() {
        const selects = timetableTable.querySelectorAll('select[name^="select1"]');
        selects.forEach(select1 => {
            select1.remove();
        });
    
        const select2s = timetableTable.querySelectorAll('select[name^="select2"]');
        select2s.forEach(select2 => {
            select2.remove();
        });

        const br = timetableTable.querySelectorAll('br');
        br.forEach(br => {
            br.remove();
        });
    }

    function displayCourses(courses) {
        if (Array.isArray(courses)) {
            console.log(courses);
            courses.forEach(course => {
                const cellId = `${course.day_of_week.toLowerCase()}-${course.time_slot}`;
                const cell = document.getElementById(cellId);
    
                if (cell) {
                    let select1 = cell.querySelector('select[name^="select1"]');
                    let select2 = cell.querySelector('select[name^="select2"]');
                    if (!select1) {
                        select1 = document.createElement('select');
                        select1.name = `select1-${cellId}`;
                        select2 = document.createElement('select');
                        select2.name = `select2-${cellId}`;
                        const defaultOption = document.createElement('option');
                        defaultOption.value = '';
                        defaultOption.textContent = '--';
                        select1.appendChild(defaultOption);
                        select2.appendChild(defaultOption);
                    }
    
                    if (course.is_required) {
                        const courseOption1 = document.createElement('option');
                        courseOption1.value = course.course_name;
                        courseOption1.textContent = course.course_name;
                        select1.appendChild(courseOption1);
                        cell.appendChild(select1);
                        const br = document.createElement('br');
                        cell.appendChild(br);
                    } else {
                        const courseOption2 = document.createElement('option');
                        courseOption2.value = course.course_name;
                        courseOption2.textContent = course.course_name;
                        select2.appendChild(courseOption2);
                    }
                    cell.appendChild(select2);
                } else {
                    console.error('Cell not found:', cellId);
                }
            });
        } else {
            console.error('Courses is not an array:', courses);
        }
    }
    

    gradeSelect.addEventListener('change', updateSelection);
    departmentSelect.addEventListener('change', updateSelection);
    halfPeriodSelect.addEventListener('change', updateSelection);

    function updateSelection() {
        saveSelectionToLocalStorage('grade', gradeSelect.value);
        saveSelectionToLocalStorage('department', departmentSelect.value);
        saveSelectionToLocalStorage('halfPeriod', halfPeriodSelect.value);
    }

});
