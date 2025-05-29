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
        
        // Add a note about markdown and expand button
        const contentField = document.querySelector('#id_content');
        if (contentField) {
            const note = document.createElement('div');
            note.style.marginTop = '10px';
            note.style.color = '#666';
            note.innerHTML = '<strong>Note:</strong> You can use Markdown formatting in your posts. Use the Preview button to see how it will look. The preview will auto-refresh every 2 seconds. <br>Press <code>Ctrl+E</code> (or <code>Cmd+E</code> on Mac) to expand/collapse the editor.';
            contentField.parentNode.appendChild(note);
            
            // Add expand/collapse button
            const expandBtn = document.createElement('button');
            expandBtn.type = 'button';
            expandBtn.textContent = '⛶ Expand Editor';
            expandBtn.style.marginTop = '10px';
            expandBtn.style.padding = '5px 10px';
            expandBtn.style.cursor = 'pointer';
            
            let isExpanded = false;
            
            expandBtn.onclick = function() {
                if (!isExpanded) {
                    // Store original styles
                    contentField.dataset.originalHeight = contentField.style.height;
                    
                    // Expand to almost fullscreen
                    contentField.style.position = 'fixed';
                    contentField.style.top = '50px';
                    contentField.style.left = '10px';
                    contentField.style.right = '10px';
                    contentField.style.bottom = '10px';
                    contentField.style.width = 'calc(100% - 20px)';
                    contentField.style.height = 'calc(100vh - 60px)';
                    contentField.style.zIndex = '9999';
                    contentField.style.backgroundColor = 'white';
                    contentField.style.border = '2px solid #79aec8';
                    contentField.style.boxShadow = '0 0 20px rgba(0,0,0,0.5)';
                    
                    expandBtn.textContent = '✕ Collapse Editor';
                    expandBtn.style.position = 'fixed';
                    expandBtn.style.top = '10px';
                    expandBtn.style.right = '10px';
                    expandBtn.style.zIndex = '10000';
                    expandBtn.style.backgroundColor = '#79aec8';
                    expandBtn.style.color = 'white';
                    expandBtn.style.border = 'none';
                    expandBtn.style.borderRadius = '4px';
                    expandBtn.style.padding = '10px 20px';
                    
                    isExpanded = true;
                } else {
                    // Restore original styles
                    contentField.style.position = '';
                    contentField.style.top = '';
                    contentField.style.left = '';
                    contentField.style.right = '';
                    contentField.style.bottom = '';
                    contentField.style.width = '';
                    contentField.style.height = contentField.dataset.originalHeight || '';
                    contentField.style.zIndex = '';
                    contentField.style.backgroundColor = '';
                    contentField.style.border = '';
                    contentField.style.boxShadow = '';
                    
                    expandBtn.textContent = '⛶ Expand Editor';
                    expandBtn.style.position = '';
                    expandBtn.style.top = '';
                    expandBtn.style.right = '';
                    expandBtn.style.zIndex = '';
                    expandBtn.style.backgroundColor = '';
                    expandBtn.style.color = '';
                    expandBtn.style.border = '';
                    expandBtn.style.borderRadius = '';
                    expandBtn.style.padding = '5px 10px';
                    
                    isExpanded = false;
                }
            };
            
            contentField.parentNode.appendChild(expandBtn);
            
            // Add keyboard shortcut (Ctrl/Cmd + E)
            document.addEventListener('keydown', function(e) {
                if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
                    e.preventDefault();
                    expandBtn.click();
                }
            });
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