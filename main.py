import html
import os
import random
import threading
from flask import Flask, render_template_string
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CYBER TERMINAL - ADMIN PANEL VIP</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        html, body {
            background-color: #030708;
            color: #00ff66;
            font-family: 'Consolas', 'Courier New', 'Monaco', monospace;
            margin: 0;
            padding: 6px;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
        }

        .app-wrapper {
            display: flex;
            flex-direction: column;
            height: 100%;
            width: 100%;
        }

        /* HIỆU ỨNG 7 MÀU ANIMATION */
        .rainbow-text {
            background: linear-gradient(90deg, #ff0000, #ff7f00, #ffff00, #00ff00, #00f3ff, #8b00ff, #ff007f, #ff0000);
            background-size: 200% auto;
            color: transparent;
            -webkit-background-clip: text;
            background-clip: text;
            animation: rainbow 1.8s linear infinite;
            font-weight: bold;
            display: inline-block;
        }

        @keyframes rainbow {
            0% { background-position: 0% center; }
            100% { background-position: 200% center; }
        }

        .terminal-header {
            background: #090d10;
            border: 1px solid #1e2d3b;
            padding: 6px 10px;
            border-radius: 4px 4px 0 0;
            font-size: 10px;
            color: #00e5ff;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: bold;
            flex-shrink: 0;
        }

        .header-dots { display: flex; gap: 5px; }
        .dot { width: 8px; height: 8px; border-radius: 50%; }
        .dot-red { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green { background: #27c93f; }

        .status-bar {
            background: #050a0e;
            border-left: 1px solid #1e2d3b;
            border-right: 1px solid #1e2d3b;
            padding: 4px 10px;
            font-size: 10px;
            color: #61afef;
            display: flex;
            justify-content: space-between;
            flex-shrink: 0;
        }

        /* KHUNG TERMINAL HIỂN THỊ LOG */
        .terminal-window {
            flex: 1;
            background: #020405;
            border: 1px solid #1e2d3b;
            padding: 8px;
            overflow-y: auto;
            font-size: 11px;
            line-height: 1.45;
            box-shadow: inset 0 0 15px rgba(0, 243, 255, 0.05);
            margin-bottom: 6px;
        }

        /* SYNTAX HIGHLIGHTING THUẬT TOÁN HACKER */
        .c-kw { color: #c678dd; font-weight: bold; }
        .c-fn { color: #61afef; }
        .c-var { color: #e06c75; }
        .c-num { color: #d19a66; }
        .c-str { color: #98c379; }
        .c-cm { color: #5c6370; font-style: italic; }

        .log-line {
            margin-bottom: 4px;
            word-break: break-word;
        }

        .log-chat {
            background: #091218;
            border: 1px solid #00f3ff;
            border-left: 4px solid #00ff66;
            padding: 8px;
            margin: 6px 0;
            color: #ffffff;
            border-radius: 3px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 0 8px rgba(0, 255, 102, 0.15);
        }

        /* Ô NHẬP DÀNH CHO ADMIN PANEL */
        .input-box-wrapper {
            display: flex;
            align-items: center;
            background: #090d10;
            border: 1px solid #00ff66;
            border-radius: 4px;
            padding: 2px 8px;
            margin-bottom: 6px;
            flex-shrink: 0;
        }

        .admin-prefix {
            font-size: 11px;
            margin-right: 6px;
            white-space: nowrap;
        }

        .input-box-wrapper input {
            flex: 1;
            background: transparent;
            border: none;
            color: #61afef;
            font-family: inherit;
            font-size: 12px;
            outline: none;
            padding: 8px 0;
            width: 100%;
        }

        .btn-send {
            background: #00ff66;
            color: #000;
            border: none;
            font-weight: bold;
            font-size: 11px;
            padding: 6px 12px;
            border-radius: 3px;
            cursor: pointer;
            margin-left: 6px;
            white-space: nowrap;
        }

        .quick-actions {
            display: flex;
            gap: 6px;
            flex-shrink: 0;
        }

        .btn-action {
            flex: 1;
            background: #0d161f;
            color: #00f3ff;
            border: 1px solid #00f3ff;
            padding: 10px 0;
            font-family: inherit;
            font-size: 12px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 4px;
            text-align: center;
        }
        .btn-action:active { background: #00f3ff; color: #000; }
        .btn-danger { border-color: #ff5555; color: #ff5555; flex: 0.35; }

        .toast {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #00ff66;
            color: #000;
            padding: 6px 16px;
            font-weight: bold;
            border-radius: 20px;
            display: none;
            box-shadow: 0 0 10px #00ff66;
            z-index: 999;
        }
    </style>
</head>
<body>

    <div class="app-wrapper">
        <div class="terminal-header">
            <div class="header-dots">
                <div class="dot dot-red"></div>
                <div class="dot dot-yellow"></div>
                <div class="dot dot-green"></div>
            </div>
            <div><span class="rainbow-text">ADMIN PANEL TERMINAL VIP</span></div>
            <div style="color:#00ff66;">[AI ONLINE]</div>
        </div>

        <div class="status-bar">
            <div>BOT AI: <span class="rainbow-text">TOOL VIP 7 MÀU</span></div>
            <div>DATABASE: <span style="color:#00f3ff;">100,000+ KHO CÂU</span></div>
        </div>

        <div class="terminal-window" id="terminal">
            <div id="logs-container">
                <div class="log-line"><span class="c-cm">// SYSTEM INITIALIZED - BOT AI READY TO ANSWER CASINO & BACCARAT DATA...</span></div>
                <div class="log-line"><span class="rainbow-text">TOOL VIP:</span> <span style="color:#00f3ff;">Chào sếp! Đã kết nối thành công Bot AI Casino. Hãy gõ câu hỏi hoặc bấm [EXECUTE 10 O5] nhé!</span></div>
                <div class="log-line" style="color:#333;">--------------------------------------------------</div>
            </div>
        </div>

        <!-- Ô NHẬP VỚI ADMIN PANEL 7 MÀU -->
        <div class="input-box-wrapper">
            <span class="admin-prefix rainbow-text">ADMIN PANEL:~$</span>
            <input type="text" id="chat-input" placeholder="Gõ câu hỏi/lệnh (Baccarat, Casino, Kéo, Soi cầu)..." autocomplete="off">
            <button class="btn-send" id="btn-submit-chat">RUN</button>
        </div>

        <div class="quick-actions">
            <button type="button" class="btn-action" id="btn-o5">⚡ EXECUTE 10 O5</button>
            <button type="button" class="btn-action btn-danger" id="btn-clear">CLEAR</button>
        </div>
    </div>

    <div class="toast" id="toast">COPIED TO CLIPBOARD!</div>

    <script>
        const Telegram = window.Telegram.WebApp;
        Telegram.expand();

        const terminal = document.getElementById('terminal');
        const logsContainer = document.getElementById('logs-container');
        const chatInput = document.getElementById('chat-input');
        const btnSubmit = document.getElementById('btn-submit-chat');
        const btnO5 = document.getElementById('btn-o5');
        const btnClear = document.getElementById('btn-clear');

        let isGenerating = false;
        let usedSentences = new Set();

        // KHO CODE RUN HACKER ĐI KÈM
        const hackerCodeTemplates = [
            '<span class="c-kw">std::vector</span>&lt;<span class="c-kw">string</span>&gt; <span class="c-var">buffer</span> = <span class="c-fn">allocate_memory</span>(<span class="c-num">0x7FFF9D</span>);',
            '<span class="c-kw">if</span> (<span class="c-fn">wss_connect</span>(<span class="c-str">"wss://casino-live.api/v3/stream"</span>) == <span class="c-num">200</span>) {',
            '    <span class="c-fn">bypass_security_token</span>(<span class="c-str">"JWT_EXPLOIT_PAYLOAD"</span>);',
            '}',
            '<span class="c-kw">auto</span> <span class="c-var">pattern</span> = <span class="c-fn">analyze_shoe_algorithm</span>(<span class="c-str">"BACCARAT_V8"</span>, <span class="c-num">8492</span>);',
            '<span class="c-cm">// Decrypting hash seed e3b0c44298fc1c149afbf4c8996fb92427ae41e4...</span>',
            '<span class="c-kw">void</span> <span class="c-fn">inject_seed_payload</span>(<span class="c-kw">int</span> <span class="c-var">thread_id</span>, <span class="c-kw">char</span>* <span class="c-var">packet</span>);',
            '<span class="c-cm">// AI Neural Network Scanning 100,000+ Casino Data Nodes...</span>'
        ];

        // MẪU CÂU CHAT BACCARAT KÉO CA
        const xungHo = ["Sếp ơi", "Anh ơi", "Idol ơi", "Đại ca ơi", "Admin ơi", "Sếp lớn", "A ơi", "Chủ phòng", "Sếp VIP", "Idol Baccarat"];
        const napAct = ["mới nạp", "vừa vào vốn", "đã nạp sẵn", "vừa bơm thêm", "em lên vốn", "vừa vào tiền", "mới chuyển cọc"];
        const tienVon = ["500k", "1m", "2m", "3m", "5m", "10m", "15m", "20m", "50m"];
        const trangThai = ["chờ sếp hô lệnh", "chờ sếp lên live", "sẵn sàng chiến rồi", "đợi sếp phát lệnh", "chuẩn bị vào ca", "chờ kéo về bờ"];
        const hupAct = ["vừa húp gọn", "mới bú đậm", "lại cộng thêm", "ăn trọn quả", "đã bú nhẹ", "húp ngọt ngào"];
        const camXuc = ["về bờ rồi sếp", "ấm no quá anh", "uy tín quá sếp", "đẳng cấp quá idol", "ngọt lịm luôn anh", "cảm ơn sếp nhiều"];
        const hoiCau = ["tay này chốt", "ván này đánh", "cầu này bệt", "ván này theo", "tay này bẻ"];
        const cuaDat = ["Banker hay Player", "Con hay Cái", "Con luôn không", "Cái luôn không"];
        const duoiHoi = ["hả sếp ơi", "được không anh", "uy tín không sếp", "nhé đại ca"];

        function generateUniqueBaccaratSentence() {
            let sentence = "";
            let attempts = 0;
            while (attempts < 30) {
                const randType = Math.floor(Math.random() * 3);
                const x = xungHo[Math.floor(Math.random() * xungHo.length)];
                if (randType === 0) {
                    sentence = `${x} ${napAct[Math.floor(Math.random() * napAct.length)]} ${tienVon[Math.floor(Math.random() * tienVon.length)]} ${trangThai[Math.floor(Math.random() * trangThai.length)]}`;
                } else if (randType === 1) {
                    sentence = `${x} ${hupAct[Math.floor(Math.random() * hupAct.length)]} ${tienVon[Math.floor(Math.random() * tienVon.length)]} ${camXuc[Math.floor(Math.random() * camXuc.length)]}`;
                } else {
                    sentence = `${x} ${hoiCau[Math.floor(Math.random() * hoiCau.length)]} ${cuaDat[Math.floor(Math.random() * cuaDat.length)]} ${duoiHoi[Math.floor(Math.random() * duoiHoi.length)]}`;
                }
                if (!usedSentences.has(sentence)) {
                    usedSentences.add(sentence);
                    return sentence;
                }
                attempts++;
            }
            return sentence;
        }

        // HE THONG BOT AI TRẢ LỜI CÂU HỎI GAME / CASINO / BACCARAT / LỆNH TOOL
        function getAiSmartResponse(query) {
            const q = query.toLowerCase();

            if (q.includes('o5') || q.includes('10 câu') || q.includes('kéo ca')) {
                return "Lệnh O5 chuẩn bị xuất 10 câu chat Baccarat không trùng lặp. Bấm nút [EXECUTE 10 O5] để chạy tự động!";
            }
            if (q.includes('baccarat là gì') || q.includes('luật baccarat') || q.includes('luật chơi')) {
                return "Baccarat là trò chơi so điểm giữa 2 cửa: Banker (Nhà cái) và Player (Người chơi). Bên nào gần 9 điểm nhất sẽ thắng. Lá 10, J, Q, K = 0 điểm, A = 1 điểm.";
            }
            if (q.includes('banker') || q.includes('cái')) {
                return "Cửa Banker (Cái) có tỷ lệ thắng nhỉnh hơn khoảng 50.68% do quy tắc rút lá thứ 3. Thông thường sảnh sẽ thu 5% hoa hồng khi Banker thắng.";
            }
            if (q.includes('player') || q.includes('con')) {
                return "Cửa Player (Con) có tỷ lệ ăn 1:1, không mất hoa hồng. Tỷ lệ thắng xấp xỉ 49.32%.";
            }
            if (q.includes('cầu bệt') || q.includes('bệt')) {
                return "Cầu bệt là thuật ngữ chỉ một cửa (Con hoặc Cái) ra liên tiếp từ 4 đến 10+ tay. Chiến thuật tốt nhất là nương theo cầu bệt đến khi gãy.";
            }
            if (q.includes('bẻ cầu') || q.includes('bẻ')) {
                return "Bẻ cầu là đánh ngược lại xu hướng hiện tại (ví dụ bệt Cái quá dài thì đánh Con). Rủi ro rất cao nếu vốn mỏng, nên cân nhắc gấp thếp hợp lý.";
            }
            if (q.includes('quản lý vốn') || q.includes('chia vốn') || q.includes('vốn')) {
                return "Chiến thuật quản lý vốn AI gợi ý: 1. Martingale (Gấp thếp 1-2-4-8) | 2. Fibonacci | 3. Đi đều tay 2-5% tổng vốn. Luôn đặt chốt lời/chốt lỗ nghiêm ngặt!";
            }
            if (q.includes('soi cầu') || q.includes('cách soi')) {
                return "Soi cầu Baccarat dựa trên 3 bảng phụ: Bảng Cầu Ngoằn Ngoèo (Big Eye Boy), Bảng Cầu Ruồi (Small Road), và Bảng Cầu Cockroach. Tool VIP phân tích xác suất từ các thuật toán này.";
            }
            if (q.includes('lệnh') || q.includes('help') || q.includes('hướng dẫn')) {
                return "Các lệnh Bot AI hỗ trợ: Gõ 'O5' (Xuất 10 câu kéo ca), 'Soi cầu' (Phân tích cầu), 'Luật chơi' (Xem quy tắc), 'Quản lý vốn' (Mẹo đi tiền), hoặc đặt bất kỳ câu hỏi Casino nào!";
            }
            if (q.includes('tool') || q.includes('hack') || q.includes('uy tín')) {
                return "TOOL VIP 7 MÀU chạy trên thuật toán Quantum AI quét 100.000+ dữ liệu thời gian thực, độ chính xác phân tích nhịp cầu lên đến 88.5%!";
            }

            // Trả lời mặc định thông minh ngẫu nhiên từ kho 100,000+ dữ liệu Casino AI
            const generalAiAnswers = [
                `Phân tích dữ liệu AI về "${query}": Tỷ lệ nhịp cầu hiện tại đang nghiêng về xu hướng bệt ngắn. Khuyên dùng chiến thuật đi đều vốn 3%.`,
                `Hệ thống Bot AI đã ghi nhận từ khóa "${query}". Lời khuyên: Giữ vững tâm lý, đi đúng chốt lời 20% vốn/ca kéo!`,
                `Dữ liệu Baccarat Realtime: Khi gặp tín hiệu "${query}", ưu tiên soi cầu phụ 1-1 trước khi vào tiền lớn!`,
                `Bot AI trả lời: Yêu cầu "${query}" đã được phân tích qua thuật toán Matrix V8. Hệ thống gợi ý đánh theo nhịp cầu nghiêng 60% Banker.`
            ];
            return generalAiAnswers[Math.floor(Math.random() * generalAiAnswers.length)];
        }

        function scrollToBottom() {
            terminal.scrollTop = terminal.scrollHeight;
        }

        function showToast(text) {
            const toast = document.getElementById('toast');
            toast.innerText = text;
            toast.style.display = 'block';
            setTimeout(() => { toast.style.display = 'none'; }, 1200);
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('COPIED: "' + text + '"');
            });
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        function appendHackerCodeLine(codeHtml) {
            const div = document.createElement('div');
            div.className = 'log-line';
            div.innerHTML = `<span style="color:#5c6370;">[EXEC]</span> ${codeHtml}`;
            logsContainer.appendChild(div);
            scrollToBottom();
        }

        /* KHUNG CHAT VỚI LABEL TOOL VIP 7 MÀU */
        function appendChatBox(text) {
            const div = document.createElement('div');
            div.className = 'log-chat';
            div.innerHTML = `<div><span class="rainbow-text">TOOL VIP:</span> <span style="color:#ffffff;">${escapeHtml(text)}</span></div> <span style="font-size:10px; color:#00ff66; font-weight:bold;">📋 COPY</span>`;
            div.onclick = () => copyToClipboard(text);
            logsContainer.appendChild(div);
            scrollToBottom();
        }

/* XỬ LÝ KHI NGƯỜI DÙNG GỬI LỆNH/CÂU HỎI TRÊN ADMIN PANEL */
        function processSend() {
            const val = chatInput.value.trim();
            if (!val) return;

            // Dòng hiển thị của Admin Panel với chữ 7 màu
            const userDiv = document.createElement('div');
            userDiv.className = 'log-line';
            userDiv.innerHTML = `<span class="rainbow-text">ADMIN PANEL:~$</span> <span style="color:#ffffff;">${escapeHtml(val)}</span>`;
            logsContainer.appendChild(userDiv);
            chatInput.value = '';
            scrollToBottom();

            // Chạy dòng code giả lập hacker trước khi Bot AI trả lời
            setTimeout(() => {
                const randomCode = hackerCodeTemplates[Math.floor(Math.random() * hackerCodeTemplates.length)];
                appendHackerCodeLine(randomCode);
                
                setTimeout(() => {
                    if (val.toLowerCase() === 'o5') {
                        execute10O5();
                    } else {
                        // BOT AI PHÂN TÍCH VÀ TRẢ LỜI CÂU HỎI DƯỚI DẠNG TOOL VIP 7 MÀU
                        const aiReply = getAiSmartResponse(val);
                        appendChatBox(aiReply);
                    }
                }, 250);
            }, 150);
        }

        btnSubmit.addEventListener('click', processSend);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                processSend();
            }
        });

        // HÀM EXECUTE 10 CÂU O5 VỚI TOOL VIP 7 MÀU
        function execute10O5() {
            if (isGenerating) return;
            isGenerating = true;
            btnO5.disabled = true;
            btnO5.style.opacity = '0.5';

            appendHackerCodeLine('<span class="c-kw">void</span> <span class="c-fn">start_batch_injection</span>() { <span class="c-var">target</span> = <span class="c-str">"O5_BACCARAT_100K_DB"</span>; }');

            let count = 0;
            let timer = setInterval(() => {
                if (count < 10) {
                    const codeSnippet = hackerCodeTemplates[Math.floor(Math.random() * hackerCodeTemplates.length)];
                    appendHackerCodeLine(codeSnippet);

                    const sentence = generateUniqueBaccaratSentence();
                    appendChatBox(sentence);
                    
                    count++;
                    btnO5.innerText = `⏳ RUNNING (${count}/10)...`;
                } else {
                    clearInterval(timer);
                    isGenerating = false;
                    btnO5.disabled = false;
                    btnO5.style.opacity = '1';
                    btnO5.innerText = '⚡ EXECUTE 10 O5';
                    appendHackerCodeLine('<span class="c-cm">// BATCH INJECTION COMPLETED SUCCESSFULLY.</span>');
                }
            }, 600);
        }

        btnO5.addEventListener('click', execute10O5);

        btnClear.addEventListener('click', function() {
            if (isGenerating) return;
            logsContainer.innerHTML = '<div class="log-line"><span class="c-cm">// TERMINAL CLEARED BY ADMIN PANEL.</span></div>';
            scrollToBottom();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

TOKEN = os.environ.get("BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://your-app-name.onrender.com")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "menu"])
@bot.message_handler(func=lambda msg: True)
def handle_all_messages(message):
    markup = InlineKeyboardMarkup()
    web_app_info = WebAppInfo(url=RENDER_URL)
    markup.add(InlineKeyboardButton("💻 MỞ ADMIN PANEL TOOL VIP 7 MÀU", web_app=web_app_info))

    msg_text = (
        "<b>[ - ADMIN PANEL CYBER TERMINAL - ]</b>\n"
        "<code>═════════════════════════════════════</code>\n"
        "<code>Hệ thống Hacker Code & Bot AI 100,000+ Data</code>\n"
        "<code>Bấm nút bên dưới để mở Sảnh Điều Hành!</code>\n"
        "<code>═════════════════════════════════════</code>"
    )
    bot.reply_to(message, msg_text, parse_mode="HTML", reply_markup=markup)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
