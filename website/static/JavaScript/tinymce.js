tinymce.init({

    selector : "textarea.tinymce4-editor",

    setup: function (editor) {
        editor.on('change', function (e) {
            editor.save();
        });
    },

    content_css: 'css/static.css',
    height: 360,

    cleanup_on_startup: true,
    remove_trailing_brs: true,
    forced_root_block : false,
    force_br_newlines : true,
    force_p_newlines : false,
    paste_auto_cleanup_on_paste: true,
    paste_remove_styles: true,
    paste_remove_styles_if_webkit: true,

    // theme: 'advanced',
    custom_undo_redo_levels: 20,

    paste_as_text: true,

    menubar: false,
    plugins: [
            'textcolor paste save link image media preview codesample contextmenu',
            'table code lists fullscreen  insertdatetime  nonbreaking',
            'contextmenu directionality searchreplace wordcount visualblocks',
            'visualchars code fullscreen autolink lists  charmap print  hr',
            'anchor pagebreak',
            ],

    toolbar: [
        'undo redo cut copy | bold italic underline strikethrough superscript subscript ' +
        '| blockquote removeformat | alignleft alignright | aligncenter alignjustify | indent outdent | ' +
        'bullist numlist | preview | link'
    ],

});




