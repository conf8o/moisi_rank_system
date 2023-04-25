import { PostMatchResultButton } from "./post_match_result_button"

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
                                <td>{i+1}</td>
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
    const createdAt = !match ? "" : !match.created_at ? "" : "作成日時: " + match.created_at
    const committedAt = !match ? "" : !match.committed_at ? "" : "マッチング確定日時: " + match.committed_at
    const closedAt = !match ? "" : !match.closed_at ? "" : "削除日時: " + match.closed_at
    const id = !match ? "" : match.id
    const onClickCommit = props.onClickCommit
    const onClickRollback = props.onClickRollback
    const onClickPostMatchResult = props.onClickPostMatchResult
    const onClickCloseMatch = props.onClickCloseMatch
    return (
        <div>
            <h2>マッチ詳細</h2>
            { !match || Object.keys(match).length === 0 ?
                "マッチング結果を表示するには、マッチIDをクリックしてください" :
                <div>
                    { !id || closedAt ?
                        "":
                        !committedAt ?
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
                    <p>{createdAt}</p>
                    <p>{committedAt}</p>
                    {closedAt ?
                        <p>{closedAt}</p>
                        :
                        <button
                            style={{padding: "10px 16px",
                                    marginBottom: "24px",
                                    backgroundColor: "#ed1520",
                                    color: "#F0F0F0",
                                    borderRadius: "5px",
                                    border: "none",
                                    cursor: "pointer"
                            }}
                            onClick={() => {onClickCloseMatch(match)}}
                        >
                            マッチを削除する
                        </button>}
                        
                    <h3>マッチング結果</h3>
                    <div style={{marginBottom: "24px"}}>
                        <MatchParties match={match}></MatchParties>
                    </div>
                    
                    {closedAt ?
                        "":
                        <PostMatchResultButton
                            onSubmit={() => {onClickPostMatchResult(match)}}
                            enableTitle={"マッチング結果を発表する"}
                            disableTitle={"マッチを確定すると発表できるようになります"}
                            isCommitted={!!committedAt}
                            isClosed={!!closedAt}
                        ></PostMatchResultButton>}
                </div>
            }
        </div>
    )
}