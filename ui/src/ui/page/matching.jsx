import React, { useEffect, useState } from 'react'
import { fetchMatching, fetchMatch, makeMatch, commitMatch, rollbackMatch } from '../../saga/matching'
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
            setMatch(matching.match)
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
        const result = window.confirm("マッチの確定を取り消します。OKを押すと、マッチが確定が解除され、エントリー情報がもとに戻ります。直前の確定マッチ情報だけでお願いします。それ以外でやるとバグります。すみません")

        if (result) {
            await rollbackMatch(match_id)
            const matching = await fetchMatching()
            setEntries(matching.entries)
            setMatches(matching.matches)
            setMatch({})
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
                ></Match>      
            </Section>
        </div>
    )
}