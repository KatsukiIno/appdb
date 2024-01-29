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

        const containers = timetableTable.querySelectorAll('.container');
        containers.forEach(container => {
            container.remove();
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
                    if (!select1 || !select2) {
                        select1 = document.createElement('select');
                        select1.name = `select1-${cellId}`;  // 各セレクトボックスに一意の名前を設定
                        select2 = document.createElement('select');
                        select2.name = `select2-${cellId}`;
                        const defaultOption1 = document.createElement('option');
                        defaultOption1.value = '';
                        defaultOption1.textContent = '--';
                        select1.appendChild(defaultOption1);
                    
                        const defaultOption2 = document.createElement('option');
                        defaultOption2.value = '';
                        defaultOption2.textContent = '--';
                        select2.appendChild(defaultOption2);

                        const container = document.createElement('div');

                        const container1 = document.createElement('div');
                        const p1 = document.createElement('p');
                        p1.textContent = '学科専門：';
                        container1.appendChild(p1);
                        container1.appendChild(select1);

                        const container2 = document.createElement('div');
                        const p2 = document.createElement('p');
                        p2.textContent = 'その他：';
                        container2.appendChild(p2);
                        container2.appendChild(select2);

                        container.classList.add('container');
                        container1.classList.add('container1');
                        container2.classList.add('container2');
                        container.appendChild(container1);
                        container.appendChild(container2);
                        // container を cell に追加
                        cell.appendChild(container);
                    }
    
                    // データベースから取得した授業名をオプションとして追加
                    if (course.is_required) {
                        // 必修の場合はテキストボックスに表示
                        const courseOption1 = document.createElement('option');
                        courseOption1.value = course.course_name;
                        courseOption1.textContent = course.course_name;
                        select1.appendChild(courseOption1);
                    } else {
                        // 必修でない場合はセレクトボックスに表示
                        const courseOption2 = document.createElement('option');
                        courseOption2.value = course.course_name;
                        courseOption2.textContent = course.course_name;
                        select2.appendChild(courseOption2);
                    }
                    // cell.appendChild(select1);
                    // cell.appendChild(select2);
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

    // const modal = document.querySelector('.js-modal');
    // const modalButton = document.querySelector('.js-modal-button');
  
  
    // const modalClose = document.querySelector('.js-close-button');
  
    // modalButton.addEventListener('click', () => {
    //   modal.classList.add('is-open');
    // });
  
    // modalClose.addEventListener('click', () => {
    //   modal.classList.remove('is-open');
  
    // });
    const modalButtons = document.querySelectorAll('.js-modal-button');
    modalButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const modalId = button.getAttribute('data-modal-id');
            const modal = document.getElementById(modalId);

            // 対応するモーダルが存在する場合に開く
            if (modal) {
                modal.classList.add('is-open');
            }
        });
    });
    const modalCloseButtons = document.querySelectorAll('.js-close-button');
    modalCloseButtons.forEach(function (closeButton) {
        closeButton.addEventListener('click', function () {
            const modal = closeButton.closest('.js-modal');
            if (modal) {
                modal.classList.remove('is-open');
            }
        });
    });

    let selectedCourseData = {};

    const addCourseButton = document.getElementById('addNewCourse');
    addCourseButton.addEventListener('click', () => {
        const grade = document.getElementById('grade').value;
        const department = document.getElementById('department').value;
        const dayOfWeek = document.getElementById('dayOfWeek').value;
        const timeSlot = document.getElementById('timeSlot').value;
        const halfPeriod = document.getElementById('halfPeriod').value;
        const courseName = document.getElementById('courseName').value;
        const courseType = document.getElementById('courseType').value;

        let errorMessage = '';

        // 各項目が未入力の場合、エラーメッセージを追加
        if (!grade) {
            errorMessage += '学年を入力してください。\n';
        }
        if (!department) {
            errorMessage += '学科を入力してください。\n';
        }
        if (!dayOfWeek) {
            errorMessage += '曜日を入力してください。\n';
        }
        if (!timeSlot) {
            errorMessage += '時限を入力してください。\n';
        }
        if (!halfPeriod) {
            errorMessage += '前期/後期を入力してください。\n';
        }
        if (!courseName) {
            errorMessage += '講義名を入力してください。\n';
        }
        if (!courseType) {
            errorMessage += '講義タイプを入力してください。\n';
        }
    
        // エラーメッセージがあれば表示して処理中断
        if (errorMessage) {
            alert(errorMessage);
            return;
        }

        // サーバーにデータを送信
        fetch('/add_new_course', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                grade,
                department,
                dayOfWeek,
                timeSlot,
                halfPeriod,
                courseName,
                course_type: courseType,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert(data.message);
            updateTimetable();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });


// script.js

    function debounce(func, wait) {
        let timeout;

        return function (...args) {
            const context = this;

            clearTimeout(timeout);
            timeout = setTimeout(() => {
                func.apply(context, args);
            }, wait);
        };
    }

    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const tableSelect = document.getElementById('courseType-delete');  // 追加
    
    searchInput.addEventListener('input', debounce(() => {
        const searchTerm = searchInput.value;
        const selectedTable = tableSelect.value;
    
        // テーブルタイプが選択されていない場合はエラーを表示
        if (!selectedTable) {
            console.error('Table type is required.');
            return;
        }
    
        // サーバーに検索クエリとテーブルタイプを送信
        fetch(`/search_courses?search_term=${searchTerm}&table_type=${selectedTable}`)
            .then(response => response.json())
            .then(data => {
                // 検索結果を表示
                showResults(data.results);
            })
            .catch(error => console.error('Error:', error));
    }, 300));
    
    

    function showResults(results) {
        // 検索結果を表示する前に既存のリストをクリア
        searchResults.innerHTML = '';
    
        // 結果が空でない場合にリストアイテムを生成して追加
        if (results.length > 0) {
            results.forEach(result => {
                const listItem = document.createElement('li');
                listItem.classList.add('selectable-item');
                // ここで適切なプロパティを表示するように変更
                if(tableSelect.value != 'general') {
                    listItem.textContent = `講義名: ${result.course_name}, 学年: ${result.grade}, 学科: ${result.department}, 曜日: ${result.day_of_week}, 時限: ${result.time_slot}, 半期: ${result.half_period}`;
                } else {
                    listItem.textContent = `講義名: ${result.course_name}, 曜日: ${result.day_of_week}, 時限: ${result.time_slot}, 半期: ${result.half_period}`;
                }
                
                searchResults.appendChild(listItem);
                listItem.addEventListener('click', () => selectCourse(result));
                searchResults.appendChild(listItem);
            });
        } else {
            // 空の場合はメッセージを表示
            const messageItem = document.createElement('li');
            messageItem.textContent = '見つかりません';
            searchResults.appendChild(messageItem);
        }
    }
    
    const selectedCourse = document.getElementById('selectedCourse');

    function selectCourse(course) {
        // 選択された講義名をコンソールに出力（適切な処理に変更することができます）
        const courseType = document.getElementById('courseType-delete').value;
        console.log('Selected Course:', course + '履修区分:', courseType);
        if(tableSelect.value != 'general') {
            selectedCourse.textContent = `講義名: ${course.course_name}, 学年: ${course.grade}, 学科: ${course.department}, 曜日: ${course.day_of_week}, 時限: ${course.time_slot}, 半期: ${course.half_period}`;
        } else {
            selectedCourse.textContent = `講義名: ${course.course_name}, 曜日: ${course.day_of_week}, 時限: ${course.time_slot}, 半期: ${course.half_period}`;
        }
    
        selectedCourseData = {
            courseName: course.course_name,
            grade: course.grade,
            department: course.department,
            dayOfWeek: course.day_of_week,
            timeSlot: course.time_slot,
            halfPeriod: course.half_period,
            courseType: courseType,
        };
        // ここで選択された講義名を利用して任意の処理を行うことができます
    }

    const deleteCourseButton = document.getElementById('deleteCourseButton');
    deleteCourseButton.addEventListener('click', () => {
        const courseNameToDelete = document.getElementById('selectedCourse').textContent;

    if (courseNameToDelete) {
        // サーバーサイドに削除リクエストを送信
        fetch('/delete_course', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                selectedCourseData
            ),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert(data.message);
            // 成功した場合、授業の表示を更新などの処理を行う
            updateTimetable(); // 例: タイムテーブルの更新
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('講義名を入力してください。');
    }
    });
    
    


});