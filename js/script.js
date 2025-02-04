// 選擇所有 tab 按鈕和內容區域
const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.tab-content');

// 為每個 tab 監聽點擊事件
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // 移除所有 tab 和內容的 active 樣式
        tabs.forEach(t => t.classList.remove('active'));
        contents.forEach(c => c.classList.remove('active'));

        // 為目前點擊的 tab 加上 active 樣式
        tab.classList.add('active');

        // 顯示對應的內容區域
        const target = tab.getAttribute('data-tab'); // 獲取 data-tab 的值
        document.getElementById(target).classList.add('active');
    });
});
