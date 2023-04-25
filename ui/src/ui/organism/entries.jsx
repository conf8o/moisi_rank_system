export const Entries = (props) => {
    const entries = props.entries
    const onClickMakeMatch = props.onClickMakeMatch
    return (
        <div>
            <h2 style={{marginBottom: "16px"}}>
                エントリー一覧
            </h2>

            <button
                style={{padding: "6px 12px",
                        marginBottom: "12px"}}
                onClick={() => onClickMakeMatch()}
            >
                マッチングを開始
            </button>

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
                    { !entries ?
                        "まだ登録されていません（またはロード中）" :
                        entries.map((entry, i) => {
                            const players = entry.players
                            return (
                                <tr>
                                    <td>{i+1}</td>
                                    { players.map( player => {
                                        return (
                                            <td style={{width: "130px"}}>
                                                {player.name + "(" + player.point + "px)"}
                                            </td>
                                        )
                                    })}
                                </tr>
                            )
                        })
                    }
                </tbody>
            </table>
        </div>
    )
}
