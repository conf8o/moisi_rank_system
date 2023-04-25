import { useState } from "react"

export const Matches = (props) => {
    const [showClosed, setShowClosed] = useState(false)
    const matches = props.matches.filter(match => !match.closed_at || showClosed)
    const onClickMatch = props.onClickMatch

    return (
        <div>
            <h2 style={{marginBottom: "16px"}}>
                マッチ一覧
            </h2>
            <input
                type="checkbox"
                id="showClosed"
                onClick={() => setShowClosed(!showClosed)}
            />
            <label for="showClosed"> 削除したマッチを表示する </label>
            <ul>
                { !matches || matches.length === 0 ?
                    "まだ登録されていません（またはロード中）":
                    matches.map(match => {
                        return (
                            <li style={{marginBottom: "16px"}}>
                                <div
                                    onClick={() => onClickMatch(match.id)}
                                    style={{color: "#2222dd",
                                            cursor: "pointer",
                                            borderBottom: "1px solid #2222dd"
                                    }}
                                >
                                    { match.id }
                                </div>
                                <div style={{fontSize: "14px"}}>{ (!match.created_at ? "" : "作成日時: " + match.created_at) }</div>
                                <div style={{fontSize: "14px"}}>{ (!match.closed_at ? "" : "削除日時: " + match.closed_at) }</div>
                            </li>
                        )
                    })
                }
            </ul>
        </div>
    )
}
