// @codekit-prepend '../../../origin.fm/assets/js/theme.js';
// @codekit-prepend '../vendor/clipboardjs/clipboard.js';

$(document).ready(
    function () {
        new ClipboardJS('[data-clipboard-text]').on(
            'success',
            function () {
                $('.feed-url').addClass('copied')
                setTimeout(
                    function () {
                        $('.feed-url').removeClass('copied')
                    },
                    1000
                )
            }
        )
    }
)
