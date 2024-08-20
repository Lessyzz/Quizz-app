function createLeaderboaard(users) {

    const content = users.sort((a, b) => a[1] - b[1]).map(user => `<li><span>${user[0]}</span> <span>${user[1]}puan</span></li>`).join("\n")

    return `
        <div class="leaderboard">
            <style>
                .leaderboard {
                    flex: 1;
                    overflow-y: auto;
                }

                .leaderboard h1 {
                    margin: 0;
                    padding-bottom: 20px;
                    border-bottom: 2px solid var(--col-4);
                    color: #fff;
                    font-size: 28px;
                    text-align: center;
                }

                .leaderboard ul {
                    list-style-type: none;
                    padding: 0;
                    margin: 20px 0;
                }

                .leaderboard li {
                    background-color: var(--container-o);
                    margin: 10px 0;
                    padding: 15px;
                    border-radius: 50px;
                    font-size: 18px;
                    color: #fff;
                    display: flex;
                    justify-content: space-between;
                }

                .leaderboard li:nth-child(1) {
                    color: rgb(221, 151, 0);
                }

                .leaderboard li:nth-child(2) {
                    color: rgb(194, 183, 255);
                }

                .leaderboard li:nth-child(3) {
                    color: rgb(226, 164, 128);
                }
            </style>
            <h1>Skor Tablosu</h1>
            <ul>
            ${content}
            </ul>
        </div>`
}