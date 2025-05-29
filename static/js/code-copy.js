// Add copy buttons and line numbers to code blocks
document.addEventListener('DOMContentLoaded', function() {
    const codeBlocks = document.querySelectorAll('.highlight');
    
    codeBlocks.forEach(function(codeBlock) {
        // Add line numbers
        addLineNumbers(codeBlock);
        
        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.textContent = 'Copy';
        copyButton.setAttribute('type', 'button');
        
        // Add click handler
        copyButton.addEventListener('click', function() {
            // Get the code text without line numbers
            const codeLines = codeBlock.querySelectorAll('.code-line');
            const codeText = Array.from(codeLines).map(line => {
                const codeContent = line.querySelector('.code-content');
                return codeContent ? codeContent.textContent : '';
            }).join('\n');
            
            // Copy to clipboard
            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(codeText).then(function() {
                    showCopiedState(copyButton);
                }).catch(function(err) {
                    console.error('Failed to copy: ', err);
                    fallbackCopy(codeText, copyButton);
                });
            } else {
                fallbackCopy(codeText, copyButton);
            }
        });
        
        // Add button to code block
        codeBlock.appendChild(copyButton);
    });
    
    function addLineNumbers(codeBlock) {
        const pre = codeBlock.querySelector('pre');
        if (!pre) return;
        
        const codeContent = pre.innerHTML;
        const lines = codeContent.split('\n');
        
        // Clear the pre content
        pre.innerHTML = '';
        
        // Add each line with line number
        lines.forEach(function(line, index) {
            if (index === lines.length - 1 && line.trim() === '') {
                return; // Skip empty last line
            }
            
            const lineDiv = document.createElement('div');
            lineDiv.className = 'code-line';
            
            const lineNumber = document.createElement('span');
            lineNumber.className = 'line-number';
            lineNumber.textContent = (index + 1).toString();
            
            const codeSpan = document.createElement('span');
            codeSpan.className = 'code-content';
            codeSpan.innerHTML = line || ' '; // Preserve empty lines
            
            lineDiv.appendChild(lineNumber);
            lineDiv.appendChild(codeSpan);
            pre.appendChild(lineDiv);
        });
    }
    
    function showCopiedState(button) {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copied');
        
        setTimeout(function() {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    }
    
    function fallbackCopy(text, button) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            showCopiedState(button);
        } catch (err) {
            console.error('Fallback copy failed: ', err);
        }
        
        document.body.removeChild(textArea);
    }
});