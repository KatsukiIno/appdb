// script.js

function saveSelectionToLocalStorage(selectName, selectedValue) {
    localStorage.setItem(selectName, selectedValue);
}

// ローカルストレージから選択内容を取得
function getSelectionFromLocalStorage(selectName) {
    return localStorage.getItem(selectName);
}

document.addEventListener('DOMContentLoaded', function () {
    const gradeSelect = document.querySelector('select[name="grade"]');
    const departmentSelect = document.querySelector('select[name="department"]');
    const halfPeriodSelect = document.querySelector('select[name="halfPeriod"]');
    const timetableTable = document.querySelector('table');

    // イベントリスナーの追加
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

    // 初回の授業更新
    updateTimetable();

    async function updateTimetable() {
        const grade = gradeSelect.value;
        const department = departmentSelect.value;
        const halfPeriod = halfPeriodSelect.value;
        console.log(grade + "" + department + "" + halfPeriod);
    
        // テーブルの内容をクリア
        clearTimetable();
    
        // サーバーにリクエストを送信
        const response = await fetch('/get_courses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `grade=${grade}&department=${department}&halfPeriod=${halfPeriod}`,
        });
    
        if (response.ok) {
            const responseData = await response.json();
    
            // 取得した授業情報をテーブルに表示
            displayCourses(responseData.courses);  // responseData.coursesを渡す
        } else {
            console.error('Failed to fetch courses');
        }
    }

    function clearTimetable() {
        // テーブル内のセレクトボックスをクリア
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
            // coursesが配列であることを確認
            // 各セルに対して授業を追加
            courses.forEach(course => {
                const cellId = `${course.day_of_week.toLowerCase()}-${course.time_slot}`;
                const cell = document.getElementById(cellId);
    
                if (cell) {
                    // 既存のセレクトボックスを取得または作成
                    let select1 = cell.querySelector('select[name^="select1"]');
                    let select2 = cell.querySelector('select[name^="select2"]');
                    if (!select1) {
                        select1 = document.createElement('select');
                        select1.name = `select1-${cellId}`;  // 各セレクトボックスに一意の名前を設定
                        select2 = document.createElement('select');
                        select2.name = `select2-${cellId}`;
                        const defaultOption = document.createElement('option');
                        defaultOption.value = '';
                        defaultOption.textContent = '--';
                        select1.appendChild(defaultOption);
                        select2.appendChild(defaultOption);
                    }
    
                    // データベースから取得した授業名をオプションとして追加
                    if (course.is_required) {
                        // 必修の場合はテキストボックスに表示
                        const courseOption1 = document.createElement('option');
                        courseOption1.value = course.course_name;
                        courseOption1.textContent = course.course_name;
                        select1.appendChild(courseOption1);
                        cell.appendChild(select1);
                        const br = document.createElement('br');
                        cell.appendChild(br);
                    } else {
                        // 必修でない場合はセレクトボックスに表示
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

    // 選択内容が変更されたときにローカルストレージに保存
    function updateSelection() {
        saveSelectionToLocalStorage('grade', gradeSelect.value);
        saveSelectionToLocalStorage('department', departmentSelect.value);
        saveSelectionToLocalStorage('halfPeriod', halfPeriodSelect.value);
    }

});
