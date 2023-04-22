export const Matches = (props) => {
    const matches = props.matches
    const onClickMatch = props.onClickMatch
    return (
        <div>
            <h2 style={{marginBottom: "16px"}}>
                マッチID
            </h2>
            <ul>
                { !matches || matches.length === 0 ?
                    "まだ登録されていません（またはロード中）":
                    matches.map(match => {
                        return (
                            <li style={{marginBottom: "12px"}}>
                                <div
                                    onClick={() => onClickMatch(match.id)}
                                    style={{color: "#2222dd",
                                            cursor: "pointer",
                                            borderBottom: "1px solid #2222dd"
                                    }}
                                >
                                    { match.id }
                                </div>
                                <div>{ (!match.created_at ? "" : "作成日時: " + match.created_at) }</div>
                            </li>
                        )
                    })
                }
            </ul>
        </div>
    )
}
