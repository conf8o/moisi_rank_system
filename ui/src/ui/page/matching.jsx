import React, { useEffect, useState } from 'react'
import { fetchMatching, fetchMatch, makeMatch, commitMatch, rollbackMatch, closeMatch } from '../../saga/matching'
import { Entries } from '../organism/entries'
import { Matches } from '../organism/matches'
import { Match } from '../organism/match'

const Section = (props) => {
    return (
        <div
            style={{
                padding: "16px 32px",
                borderRight: props.is_last ? undefined : "1px solid"
            }}  
        >
            { props.children }
        </div>
    )
}

export const MatchingUI = () => {
    const [entries, setEntries] = useState([])
    const [matches, setMatches] = useState([])
    const [match, setMatch] = useState({})
    
    const onClickMatch = async (id) => {
        const match = await fetchMatch(id)
        setMatch(match)
    }

    const onClickMakeMatch = async () => {
        const result = window.confirm("マッチングを開始します。OKを押すと、マッチングを行い、マッチID一覧にIDが追加されます。")

        if (result) {
            await makeMatch()
            const matching = await fetchMatching()
            setEntries(matching.entries)
            setMatches(matching.matches)
        }
    }

    const onClickCommit = async (match_id) => {
        const result = window.confirm("マッチを確定します。OKを押すと、マッチが確定され、エントリー情報を消化します。")

        if (result) {
            const match = await commitMatch(match_id)
            const matching = await fetchMatching()
            setEntries(matching.entries)
            setMatches(matching.matches)
            setMatch(match)
        }
    }

    const onClickRollback = async (match_id) => {
        const result = window.confirm("マッチの確定を取り消します。OKを押すと、マッチが削除され、エントリー情報がもとに戻ります。")

        if (result) {
            await rollbackMatch(match_id)
            const matching = await fetchMatching()
            setEntries(matching.entries)
            setMatches(matching.matches)
            setMatch({})
        }
    }

    const onClickCloseMatch = async (match) => {
        const result = window.confirm("マッチを削除します。消化したエントリー情報はもとに戻りません。")
        
        if (result) {
            await closeMatch(match)
            const matching = await fetchMatching()
            setEntries(matching.entries)
            setMatches(matching.matches)
            const closedMatch = await fetchMatch(match.id)
            setMatch(closedMatch)
        }
    }

    const onClickPostMatchResult = async (match) => {
        const result1 = window.confirm("マッチの結果をDiscordに発表します。")
        if (result1) {
            const matchId = match.id
            const matchCreatedAt = match.created_at
            const result2 = window.confirm(`以下のマッチを発表します。確認ができたらOKを押してください。\n ID: ${matchId}\n作成日時: ${matchCreatedAt}`)
            if (result2) {
                console.log("ok", match)
            }
        }
    }

    useEffect(() => {
        const fetch = async () => {
            const matching = await fetchMatching()
            setEntries(matching.entries)
            setMatches(matching.matches)
        }
        fetch()
    }, [])

    return (
        <div style={{display: "flex"}}>
            <Section>
                <Entries
                    entries={entries}
                    onClickMakeMatch={onClickMakeMatch}
                ></Entries>
            </Section>
            <Section>
                <Matches
                    matches={matches}
                    onClickMatch={onClickMatch}
                ></Matches>
            </Section>
            <Section is_last={true}>
                <Match
                    match={match}
                    onClickCommit={onClickCommit}
                    onClickRollback={onClickRollback}
                    onClickCloseMatch={onClickCloseMatch}
                    onClickPostMatchResult={onClickPostMatchResult}
                ></Match>      
            </Section>
        </div>
    )
}