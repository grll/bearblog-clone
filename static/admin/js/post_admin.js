document.addEventListener('DOMContentLoaded', function() {
    // Add preview button to the form
    const submitRow = document.querySelector('.submit-row');
    if (submitRow) {
        // Get the post ID from the URL (for existing posts)
        const pathParts = window.location.pathname.split('/');
        const postId = pathParts[pathParts.length - 3]; // ID is third from end in /admin/core/post/ID/change/
        const isExistingPost = postId && !isNaN(postId);
        
        // Create preview button
        const previewBtn = document.createElement('input');
        previewBtn.type = 'button';
        previewBtn.value = 'Preview';
        previewBtn.className = 'button';
        previewBtn.style.float = 'left';
        previewBtn.style.marginRight = '10px';
        
        // Handle preview click
        previewBtn.onclick = function() {
            if (isExistingPost) {
                // For existing posts, use the preview URL
                window.open(`/admin/core/post/preview/${postId}/`, '_blank');
            } else {
                // For new posts, create a temporary preview
                const form = document.querySelector('#post_form');
                if (form) {
                    // Create a form to submit the preview data
                    const previewForm = document.createElement('form');
                    previewForm.method = 'POST';
                    previewForm.action = '/admin/core/post/preview/new/';
                    previewForm.target = '_blank';
                    
                    // Copy CSRF token
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                    if (csrfToken) {
                        previewForm.appendChild(csrfToken.cloneNode(true));
                    }
                    
                    // Copy form fields
                    const title = document.querySelector('#id_title');
                    const content = document.querySelector('#id_content');
                    
                    if (title) {
                        const titleInput = document.createElement('input');
                        titleInput.type = 'hidden';
                        titleInput.name = 'title';
                        titleInput.value = title.value || 'Untitled';
                        previewForm.appendChild(titleInput);
                    }
                    
                    if (content) {
                        const contentInput = document.createElement('textarea');
                        contentInput.name = 'content';
                        contentInput.value = content.value || '';
                        contentInput.style.display = 'none';
                        previewForm.appendChild(contentInput);
                    }
                    
                    // Submit the preview form
                    document.body.appendChild(previewForm);
                    previewForm.submit();
                    document.body.removeChild(previewForm);
                }
            }
        };
        
        // Add button to submit row
        submitRow.insertBefore(previewBtn, submitRow.firstChild);
        
        // Add a note about markdown
        const contentField = document.querySelector('#id_content');
        if (contentField) {
            const note = document.createElement('div');
            note.style.marginTop = '10px';
            note.style.color = '#666';
            note.innerHTML = '<strong>Note:</strong> You can use Markdown formatting in your posts. Use the Preview button to see how it will look. The preview will auto-refresh every 2 seconds.';
            contentField.parentNode.appendChild(note);
        }
        
        // Auto-update preview data every 2 seconds
        if (!isExistingPost) {
            setInterval(function() {
                const title = document.querySelector('#id_title');
                const content = document.querySelector('#id_content');
                
                if (title && content) {
                    // Send current form data to update session
                    const formData = new FormData();
                    formData.append('title', title.value || 'Untitled');
                    formData.append('content', content.value || '');
                    
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                    if (csrfToken) {
                        formData.append('csrfmiddlewaretoken', csrfToken.value);
                    }
                    
                    // Silent POST to update session
                    fetch('/admin/core/post/preview/new/', {
                        method: 'POST',
                        body: formData,
                        credentials: 'same-origin'
                    });
                }
            }, 2000);
        }
    }
});