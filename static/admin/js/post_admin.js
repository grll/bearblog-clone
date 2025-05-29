document.addEventListener('DOMContentLoaded', function() {
    // Add preview button to the form
    const submitRow = document.querySelector('.submit-row');
    if (submitRow) {
        // Get the post ID from the URL
        const pathParts = window.location.pathname.split('/');
        const postId = pathParts[pathParts.length - 3]; // ID is third from end in /admin/core/post/ID/change/
        
        if (postId && !isNaN(postId)) {
            // Create preview button
            const previewBtn = document.createElement('a');
            previewBtn.href = `/admin/core/post/preview/${postId}/`;
            previewBtn.target = '_blank';
            previewBtn.className = 'button';
            previewBtn.style.float = 'left';
            previewBtn.style.marginRight = '10px';
            previewBtn.textContent = 'Preview';
            
            // Add button to submit row
            submitRow.insertBefore(previewBtn, submitRow.firstChild);
            
            // Also add a note about markdown
            const contentField = document.querySelector('#id_content');
            if (contentField) {
                const note = document.createElement('div');
                note.style.marginTop = '10px';
                note.style.color = '#666';
                note.innerHTML = '<strong>Note:</strong> You can use Markdown formatting in your posts. Use the Preview button to see how it will look.';
                contentField.parentNode.appendChild(note);
            }
        }
    }
});