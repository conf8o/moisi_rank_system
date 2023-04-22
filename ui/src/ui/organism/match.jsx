const MatchParties = (props) => {
    const parties = props.match.parties
    return (
        <table>
            <thead>
                <tr>
                    <th style={{width: "65px"}}>#</th>
                    <th style={{width: "130px"}}>1</th>
                    <th style={{width: "130px"}}>2</th>
                    <th style={{width: "130px"}}>3</th>
                </tr>
            </thead>
            <tbody>
                { !parties ?
                    "まだ登録されていません（またはロード中）" :
                    parties.map((party, i) => {
                        const players = party.players
                        return (
                            <tr>
                                <td>{i}</td>
                                { players.map( player => {
                                    return (
                                        <td style={{width: "130px"}}>
                                            {player.name + "(" + player.point + "pt)"}
                                        </td>
                                    )
                                })}
                            </tr>
                        )
                    })
                }
            </tbody>
        </table>
    )
}

export const Match = (props) => {
    const match = props.match
    console.log(match)
    const created_at = !match ? "" : !match.created_at ? "" : "作成日時: " + match.created_at
    const committed_at = !match ? "" : !match.committed_at ? "" : "マッチング確定日時: " + match.committed_at
    const closed_at = !match ? "" : !match.closed_at ? "" : "削除日時" + match.closed_at
    const id = !match ? "" : match.id
    const onClickCommit = props.onClickCommit
    const onClickRollback = props.onClickRollback
    return (
        <div>
            <h2>マッチ詳細</h2>
            { !match || Object.keys(match).length === 0 ?
                "マッチング結果を表示するには、マッチIDをクリックしてください" :
                <div>
                    { !id ?
                        "":
                        !committed_at ?
                            <button
                                style={{padding: "6px 12px",
                                        marginBottom: "12px"}}
                                onClick={() => onClickCommit(id)}
                            >
                                マッチを確定
                            </button>
                            :
                            <button
                                style={{padding: "6px 12px",
                                        marginBottom: "12px"}}
                                onClick={() => onClickRollback(id)}
                            >
                                マッチの確定を取り消す
                            </button>

                    }
                    <p>{"ID: " + id}</p>
                    <p>{created_at}</p>
                    <p>{committed_at}</p>
                    <p>{closed_at}</p>
                    <MatchParties match={match}></MatchParties>
                </div>
            }
        </div>
    )
}