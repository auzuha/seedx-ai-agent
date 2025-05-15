## Structure


<pre>
MAIN DIR
    main.py - fastapi app
    /tools
        tools.py - ai tools (functions)
    /utils
        utils.py - anon utils
        graph.py - main langgraph setup
        logger.py - for logging conversation
</pre>

## Log Structure
<pre>
{
    'user_msg': str,
    'timestamp': str,
    'tool_calls': List[str],
    'final_answer': str
}
</pre>