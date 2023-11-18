// form.js

// 初始化 Firebase
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    databaseURL: "YOUR_DATABASE_URL",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};
firebase.initializeApp(firebaseConfig);

// 獲取數據庫引用
const database = firebase.database();

// 顯示名單
function showPlayerList() {
    const playerListBody = document.getElementById('playerListBody');
    // 從 Firebase 獲取數據並渲染到表格中
    database.ref('/playerList').once('value').then(snapshot => {
        snapshot.forEach(childSnapshot => {
            const data = childSnapshot.val();
            const row = document.createElement('tr');
            row.innerHTML = `<td>${data.order}</td><td>${data.name}</td><td><button onclick="deletePlayer('${childSnapshot.key}')">删除</button></td>`;
            playerListBody.appendChild(row);
        });
    });
}

// 新增新成员
function addPlayer() {
    const order = document.getElementById('order').value;
    const name = document.getElementById('name').value;

    // 將新成员新增到 Firebase 數據庫
    database.ref('/playerList').push({
        order: order,
        name: name
    });

    // 清空表單字段
    document.getElementById('order').value = '';
    document.getElementById('name').value = '';

    // 重新顯示名單
    showPlayerList();
}

// 删除成员
function deletePlayer(key) {
    // 從 Firebase 數據庫中删除成员
    database.ref(`/playerList/${key}`).remove();

    // 重新顯示名單
    showPlayerList();
}

// 初始化页面时顯示名單
showPlayerList();
