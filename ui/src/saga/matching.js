import {
    queryEntries,
    queryMatches,
    fetchMatch as asyncFetchMatch,
    makeMatch as asyncMakeMatch,
    commitMatch as asyncCommitMatch,
    rollbackMatch as asyncRollbackMatch
} from "./interface/matching";

export async function fetchMatching() {
    const entries = await queryEntries()
    const matches = await queryMatches()
    
    return {
        entries: entries,
        matches: matches
    }
}

export async function fetchMatch(id) {
    const match = await asyncFetchMatch(id)
    return match
}

export async function makeMatch() {
    const match = await asyncMakeMatch()
    return match
}

export async function commitMatch(id) {
    const match = await asyncCommitMatch(id)
    return match
}

export async function rollbackMatch(id) {
    const match = await asyncRollbackMatch(id)
    return match
}
