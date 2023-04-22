export const PostMatchResultButton = (props) => {
    const onSubmit = props.onSubmit
    const enableTitle = props.enableTitle
    const disableTitle = props.disableTitle
    const isCommitted = props.isCommitted
    const isClosed = props.isClosed

    const enabled = isCommitted && !isClosed
    return (
        <button
            style={{padding: "12px 18px",
                    marginBottom: "12px",
                    backgroundColor: enabled ? "#364ed1" : "#666666",
                    color: enabled ? "#F0F0F0" : "#333333",
                    borderRadius: "5px",
                    border: "none",
                    cursor: enabled ? "pointer": undefined
                    }}
            onClick={() => {
                if (enabled) {
                    onSubmit()
                }
            }}
            disable={ enabled ? undefined : "true" }
        >
            { enabled ? enableTitle : disableTitle }
        </button>
    )
}