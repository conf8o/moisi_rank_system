export async function queryEntries(q) {
    const qs = new URLSearchParams(q).toString()
    
    const response = await fetch("/matching/entries?" + qs, {
        method: "GET",
        headers: {"Content-Type": "application/json"}
    })
    return response.status === 200 ? response.json() : []
}

export async function queryMatches(q) {
    const qs = new URLSearchParams(q).toString()
    
    const response = await fetch("/matching/matches?" + qs, {
        method: "GET",
        headers: {"Content-Type": "application/json"}
    })

    return response.status === 200 ? response.json() : []
}

export async function fetchMatch(id) {
    const response = await fetch("/matching/matches/" + id, {
        method: "GET",
        headers: {"Content-Type": "application/json"}
    })

    return response.status === 200 ? response.json() : {}
}

export async function updateMatch(match) {
    const response = await fetch("/matching/matches/" + match.id, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(match)
    })

    return response.status === 200 ? response.json() : {}
}


export async function makeMatch() {
    const response = await fetch("/matching/match_making", {
        method: "POST",
        headers: {"Content-Type": "application/json"}
    })

    return response.status === 200 ? response.json() : []
}

export async function commitMatch(id) {
    const response = await fetch("/matching/match_committing/" + id, {
        method: "POST",
        headers: {"Content-Type": "application/json"}
    })

    return response.status === 200 ? response.json() : {}
}

export async function rollbackMatch(id) {
    const response = await fetch("/matching/match_rollbacking/" + id, {
        method: "POST",
        headers: {"Content-Type": "application/json"}
    })

    return response.status === 200 ? response.json() : {}
}

export async function postMatchResult(match_id) {
    const response = await fetch("/matching/posting_matching_result/" + match_id, {
        method: "POST",
        headers: {"Content-Type": "application/json"}
    })

    return response.status === 200 ? response.json() : {}
}
