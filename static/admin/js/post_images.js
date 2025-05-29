// Use setTimeout to ensure DOM is fully loaded and inlines are initialized
setTimeout(function() {
    // Handle PostImage inline forms - try multiple selectors
    let mainInlineGroup = document.querySelector('#postimage_set-group');
    if (!mainInlineGroup) {
        mainInlineGroup = document.querySelector('.inline-group');
        if (!mainInlineGroup) {
            setTimeout(arguments.callee, 500);
            return;
        }
    }
    
    
    // Function to add insert buttons to each image row
    function addInsertButtons() {
        const imageTable = document.querySelector('.inline-group table');
        if (!imageTable) return;
        
        // Get all rows except the header row and "Add another" row
        const allRows = imageTable.querySelectorAll('tbody tr');
        const imageRows = Array.from(allRows).filter(row => {
            return !row.textContent.includes('Add another Image') && 
                   !row.querySelector('th') && 
                   row.querySelector('input[type="file"]');
        });
        
        imageRows.forEach(function(row, index) {
            const imageField = row.querySelector('input[type="file"]');
            const captionField = row.querySelector('input[id*="caption"]');
            const orderField = row.querySelector('input[id*="order"]');
            
            if (!imageField) return;
            
            // Set default order if empty
            if (orderField && !orderField.value) {
                orderField.value = index;
            }
            
            // Check if button already exists
            if (row.querySelector('.insert-image-btn')) return;
            
            // Create insert button - always create it, enable/disable as needed
            const insertBtn = document.createElement('button');
            insertBtn.type = 'button';
            insertBtn.textContent = '📷 Insert into Content';
            insertBtn.className = 'insert-image-btn button';
            insertBtn.style.marginLeft = '10px';
            insertBtn.style.padding = '5px 10px';
            insertBtn.style.fontSize = '11px';
            
            // Check if we should enable the button
            const currentImage = row.querySelector('a[href*="/media/post_images/"]');
            const hasFileSelected = imageField.files && imageField.files.length > 0;
            
            insertBtn.disabled = !(currentImage || hasFileSelected);
            
            // Enable button when new image is selected
            imageField.addEventListener('change', function() {
                insertBtn.disabled = !this.value;
                
                // For new posts, auto-upload the image when selected
                if (this.files && this.files[0] && window.location.pathname.includes('/add/')) {
                    const formData = new FormData();
                    formData.append('image', this.files[0]);
                    
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                    if (csrfToken) {
                        formData.append('csrfmiddlewaretoken', csrfToken.value);
                    }
                    
                    // Upload image immediately for preview purposes
                    fetch('/admin/core/post/upload-image/', {
                        method: 'POST',
                        body: formData,
                        credentials: 'same-origin'
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Store the uploaded image URL on the row for use in preview
                            row.dataset.uploadedImageUrl = data.url;
                            insertBtn.disabled = false;
                            
                            // Update the help text to show the image was uploaded
                            const helpText = row.querySelector('.image-upload-help');
                            if (helpText) {
                                helpText.innerHTML = `✅ Image uploaded: <a href="${data.url}" target="_blank">${data.filename}</a>`;
                            }
                        }
                    })
                    .catch(error => {
                        const helpText = row.querySelector('.image-upload-help');
                        if (helpText) {
                            helpText.innerHTML = '❌ Upload failed. Image will be available after saving the post.';
                        }
                    });
                }
            });
            
            // Handle insert click
            insertBtn.onclick = function() {
                let imageUrl = '';
                let altText = '';
                
                // Get the image URL
                const existingImage = row.querySelector('a[href*="/media/post_images/"]');
                if (existingImage) {
                    imageUrl = existingImage.href;
                } else if (row.dataset.uploadedImageUrl) {
                    // For new posts with auto-uploaded image
                    imageUrl = row.dataset.uploadedImageUrl;
                } else if (imageField.files && imageField.files[0]) {
                    // For new uploads, use a placeholder (will work after save)
                    const fileName = imageField.files[0].name;
                    imageUrl = `/media/post_images/${fileName}`;
                }
                
                // Get alt text from caption or use default
                if (captionField && captionField.value) {
                    altText = captionField.value;
                } else {
                    altText = `Image ${(index + 1)}`;
                }
                
                if (imageUrl) {
                    const imageMarkdown = `![${altText}](${imageUrl})`;
                    
                    // Find the main content field
                    const contentField = document.querySelector('#id_content');
                    if (contentField) {
                        // Insert at cursor position or append
                        const cursorPos = contentField.selectionStart || contentField.value.length;
                        const textBefore = contentField.value.substring(0, cursorPos);
                        const textAfter = contentField.value.substring(cursorPos);
                        
                        contentField.value = textBefore + '\n\n' + imageMarkdown + '\n\n' + textAfter;
                        contentField.focus();
                        
                        // Update cursor position
                        const newPos = cursorPos + imageMarkdown.length + 4;
                        contentField.setSelectionRange(newPos, newPos);
                    }
                }
            };
            
            // Add button to the image field's cell
            const imageCell = imageField.closest('td');
            if (imageCell) {
                imageCell.appendChild(insertBtn);
            }
            
            // Add help text for upload status
            const helpText = document.createElement('div');
            helpText.className = 'image-upload-help';
            helpText.style.marginTop = '5px';
            helpText.style.fontSize = '11px';
            helpText.style.color = '#666';
            
            if (currentImage) {
                helpText.innerHTML = `✅ Image available: <a href="${currentImage.href}" target="_blank">${currentImage.textContent}</a>`;
            } else {
                helpText.innerHTML = '📁 Select an image to upload and insert into content';
            }
            
            if (imageCell) {
                imageCell.appendChild(helpText);
            }
        });
    }
    
    // Add buttons initially and after a short delay for DOM changes
    addInsertButtons();
    setTimeout(addInsertButtons, 2000);
    
    // Re-add buttons when new inline forms are added
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.classList.contains('form-row')) {
                        setTimeout(addInsertButtons, 100);
                    }
                });
            }
        });
    });
    
    observer.observe(mainInlineGroup, {
        childList: true,
        subtree: true
    });
    
    // Add a "Insert All Images" button
    if (mainInlineGroup) {
        const insertAllBtn = document.createElement('button');
        insertAllBtn.type = 'button';
        insertAllBtn.textContent = '📷 Insert All Images';
        insertAllBtn.className = 'button';
        insertAllBtn.style.marginTop = '10px';
        insertAllBtn.style.marginBottom = '10px';
        
        insertAllBtn.onclick = function() {
            const imageTable = document.querySelector('.inline-group table');
            if (!imageTable) return;
            
            const allRows = imageTable.querySelectorAll('tbody tr');
            const imageRows = Array.from(allRows).filter(row => {
                return !row.textContent.includes('Add another Image') && 
                       !row.querySelector('th') && 
                       row.querySelector('input[type="file"]');
            });
            
            let allImagesMarkdown = '';
            
            imageRows.forEach(function(row, index) {
                const existingImage = row.querySelector('a[href*="/media/post_images/"]');
                const captionField = row.querySelector('input[id*="caption"]');
                let imageUrl = '';
                
                // Get image URL from existing image or uploaded URL
                if (existingImage) {
                    imageUrl = existingImage.href;
                } else if (row.dataset.uploadedImageUrl) {
                    imageUrl = row.dataset.uploadedImageUrl;
                }
                
                if (imageUrl) {
                    let altText = '';
                    if (captionField && captionField.value) {
                        altText = captionField.value;
                    } else {
                        altText = `Image ${index + 1}`;
                    }
                    
                    allImagesMarkdown += `![${altText}](${imageUrl})\n\n`;
                }
            });
            
            if (allImagesMarkdown) {
                const contentField = document.querySelector('#id_content');
                if (contentField) {
                    const cursorPos = contentField.selectionStart || contentField.value.length;
                    const textBefore = contentField.value.substring(0, cursorPos);
                    const textAfter = contentField.value.substring(cursorPos);
                    
                    contentField.value = textBefore + '\n\n' + allImagesMarkdown + textAfter;
                    contentField.focus();
                    
                    const newPos = cursorPos + allImagesMarkdown.length + 2;
                    contentField.setSelectionRange(newPos, newPos);
                }
            }
        };
        
        // Add the button after the table
        const table = mainInlineGroup.querySelector('table');
        if (table) {
            table.parentNode.insertBefore(insertAllBtn, table.nextSibling);
        }
    }
}, 1000);  // Initial delay of 1 second