# Email Feature Demo

This file demonstrates how the new email feature works in the Embergard Card Bot.

## Usage Examples
### Example: Rules question
```
[[Rules Question: Wurmspat - Blades of Putrefaction]]
"Friendly fighters' melee weapons have Grievous in addition to any other weapon abilities in the next turn." 
This still means RAW that you can only pick one weapon ability, right? 
It doesn't mean that you can apply this in addition to another weapon ability? 
```

## How It Works

1. **Pattern Recognition**: The bot looks for messages with the pattern `[[Subject]]` followed by content
2. **Email Generation**: Creates a `mailto:` link to `whunderworlds§at§gwplc.com` with the subject and body
3. **Discord Response**: Sends an embed with the email details and a clickable link
4. **User Action**: Clicking the link opens the default email client with pre-filled content

## Benefits

- **Easy Reporting**: Users can quickly ask questions or report unintended card interactions
- **Structured Communication**: Encourages clear subject lines and detailed descriptions
- **No Account Required**: Works with any email client
- **Preserves Context**: All communication goes through official channels