"use strict";
var skillsColor;
var skillsFill;

jQuery(document).on('ready', function () {

    jQuery(window).on('scroll', function () {
        animateElement();
    });

    //Fix for Split Section Backgroun on small resolutions
    setBackgroundColorSplitSection();
    //Fix for V-Skills
    verticalSkills();
    //Fix z-index
    zIndexSectionFix();
    //Member Content Load
    memberContentLoadOnClick();
    //Portfolio Item Load
    portfolioItemContentLoadOnClick();
    //PrettyPhoto initial    
    setPrettyPhoto();


    //Fix for Menu
    jQuery(".header-holder").sticky({topSpacing: 0});

    //Slow Scroll
    jQuery('#header-main-menu ul li a, .scroll').on("click", function (e) {
        if (jQuery(this).attr('href') === '#')
        {
            e.preventDefault();
        } else {
            if (jQuery(window).width() < 1024) {
                if (!jQuery(e.target).is('.sub-arrow'))
                {
                    jQuery('html, body').animate({scrollTop: jQuery(this.hash).offset().top - 77}, 1500);
                    jQuery('.menu-holder').removeClass('show');
                    jQuery('#toggle').removeClass('on');
                    return false;
                }
            } else
            {
                jQuery('html, body').animate({scrollTop: jQuery(this.hash).offset().top - 77}, 1500);
                return false;
            }
        }
    });

    //Logo Click Fix
    jQuery('.header-logo').on("click", function (e) {
        if (jQuery(".page-template-onepage").length) {
            e.preventDefault();
            jQuery('html, body').animate({scrollTop: 0}, 1500);
        }
    });

    jQuery(window).scrollTop(1);
    jQuery(window).scrollTop(0);

    jQuery('.single-post .num-comments a').on('click', function (e) {
        e.preventDefault();
        jQuery('html, body').animate({scrollTop: jQuery(this.hash).offset().top}, 2000);
        return false;
    });


    //Placeholder show/hide
    jQuery('input, textarea').on("focus", function () {
        jQuery(this).data('placeholder', jQuery(this).attr('placeholder'));
        jQuery(this).attr('placeholder', '');
    });
    jQuery('input, textarea').on("blur", function () {
        jQuery(this).attr('placeholder', jQuery(this).data('placeholder'));
    });

    //Fit Video
    jQuery(".site-content").fitVids();

    //Fix for Default menu
    jQuery(".default-menu ul:first").addClass('sm sm-clean main-menu');

    //Set menu
    jQuery('.main-menu').smartmenus({
        subMenusSubOffsetX: 1,
        subMenusSubOffsetY: -8,
        markCurrentTree: true
    });

    var $mainMenu = jQuery('.main-menu').on('click', 'span.sub-arrow', function (e) {
        var obj = $mainMenu.data('smartmenus');
        if (obj.isCollapsible()) {
            var $item = jQuery(this).parent(),
                    $sub = $item.parent().dataSM('sub');
            $sub.dataSM('arrowClicked', true);
        }
    }).bind({
        'beforeshow.smapi': function (e, menu) {
            var obj = $mainMenu.data('smartmenus');
            if (obj.isCollapsible()) {
                var $menu = jQuery(menu);
                if (!$menu.dataSM('arrowClicked')) {
                    return false;
                }
                $menu.removeDataSM('arrowClicked');
            }
        }
    });


    //Show-Hide header sidebar
    jQuery('#toggle').on('click', multiClickFunctionStop);

});



jQuery(window).on('load', function () {
    //Set Istope Layout on Portfolio
    isotopeSetUp();

    // Animate the elemnt if is allready visible on load
    animateElement();

    //Fix for hash
    var hash = location.hash;
    if ((hash != '') && (jQuery(hash).length))
    {
        jQuery('html, body').animate({scrollTop: jQuery(hash).offset().top - 77}, 1);
    }

    //Slider Image Set Up
    imageSliderSettings();

    jQuery('.doc-loader').fadeOut(600);
});





//------------------------------------------------------------------------
//Helper Methods -->
//------------------------------------------------------------------------


var animateElement = function (e) {
    jQuery(".animate").each(function (i) {
        var top_of_object = jQuery(this).offset().top;
        var bottom_of_window = jQuery(window).scrollTop() + jQuery(window).height();
        if ((bottom_of_window - 70) > top_of_object) {
            jQuery(this).addClass('show-it');
        }
    });
};

var setBackgroundColorSplitSection = function () {
    jQuery(".section-title-holder").each(function () {
        jQuery(this).css("background-color", jQuery(this).data("background"));
    });
};

var verticalSkills = function () {
    jQuery(".v-skill").each(function (i) {
        skillsColor = jQuery(this).find('span').data("color");
        skillsFill = jQuery(this).find('span').html();
        jQuery(this).find('.v-skill-fill').css("background-color", skillsColor).width(skillsFill).height(skillsFill);
        jQuery(this).find('.v-skill-text').css("bottom", skillsFill);
        jQuery(this).find('span').css("color", skillsColor);
    });
};


var multiClickFunctionStop = function (e) {
    jQuery('#toggle').off("click");
    jQuery('#toggle').toggleClass("on");
    if (jQuery('#toggle').hasClass("on"))
    {
        jQuery('.menu-holder').addClass('show');
        jQuery('#toggle').on("click", multiClickFunctionStop);
    } else
    {
        jQuery('.menu-holder').removeClass('show');
        jQuery('#toggle').on("click", multiClickFunctionStop);
    }
};


jQuery(window).on('scroll resize', function () {
    var currentSection = null;
    jQuery('.section, footer').each(function () {
        var element = jQuery(this).attr('id');
        if (jQuery('#' + element).is('*')) {
            if (jQuery(window).scrollTop() >= jQuery('#' + element).offset().top - 115)
            {
                currentSection = element;
            }
        }
    });

    jQuery('#header-main-menu ul li').removeClass('active').find('a[href*="#' + currentSection + '"]').parent().addClass('active');
});

function imageSliderSettings() {
    jQuery(".image-slider").each(function () {
        var id = jQuery(this).attr('id');
        var auto_value = window[id + '_auto'];
        var hover_pause = window[id + '_hover'];
        var speed_value = window[id + '_speed'];
        var items_value = window[id + '_items'];
        auto_value = (auto_value === 'true') ? true : false;
        hover_pause = (hover_pause === 'true') ? true : false;
        jQuery('#' + id).owlCarousel({
            loop: true,
            autoHeight: true,
            smartSpeed: 750,
            autoplay: auto_value,
            autoplayHoverPause: hover_pause,
            autoplayTimeout: speed_value,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1
                },
                1024: {
                    items: items_value,
                }
            }
        });
        jQuery(this).on('mouseleave', function () {
            jQuery(this).trigger('stop.owl.autoplay');
            jQuery(this).trigger('play.owl.autoplay', [auto_value]);
        })
    });
}

function zIndexSectionFix() {
    var numSection = jQuery(".page-template-onepage .section-wrapper").length + 2;
    jQuery('.page-template-onepage').find('.section-wrapper').each(function () {
        jQuery(this).css('zIndex', numSection);
        numSection--;
    });
}

function memberContentLoadOnClick() {
    jQuery('.ajax-member-content').on('click', function (e) {
        e.preventDefault();
        var memberID = jQuery(this).data('id');
        jQuery(this).find('.member-mask').addClass('animate-plus');
        jQuery('html, body').animate({scrollTop: jQuery('#team-holder').offset().top - 120}, 300);
        if (jQuery("#mcw-" + memberID).length) //Check if is allready loaded
        {
            setTimeout(function () {
                jQuery('.member-holder').addClass('hide');
                setTimeout(function () {
                    jQuery("#mcw-" + memberID).addClass('show');
                    jQuery('.team-load-content-holder').addClass('show');
                    jQuery('.member-mask').removeClass('animate-plus');
                    jQuery('.member-holder').hide();
                }, 300);
            }, 300);
        } else {
            loadMemberContent(memberID);
        }
    });
}

function loadMemberContent(memberID) {
    jQuery.ajax({
        url: jQuery('.ajax-member-content[data-id="' + memberID + '"]').attr('href'),
        type: 'POST',
        success: function (html) {
            var getHtml = jQuery(html).find(".member-item-wrapper").html();
            jQuery('.team-load-content-holder').append('<div id="mcw-' + memberID + '" class="member-content-wrapper">' + getHtml + '</div>');
            if (!jQuery("#mcw-" + memberID + " .close-icon").length) {
                jQuery("#mcw-" + memberID).prepend('<div class="close-icon"></div>');
            }
            jQuery("#mcw-" + memberID).imagesLoaded(function () {
                verticalSkills();
                imageSliderSettings();
                jQuery(".site-content").fitVids(); //Fit Video                
                jQuery('.member-holder').addClass('hide');
                setTimeout(function () {
                    jQuery("#mcw-" + memberID).addClass('show');
                    jQuery('.team-load-content-holder').addClass('show');
                    jQuery('.member-mask').removeClass('animate-plus');
                    jQuery('.member-holder').hide();
                }, 300);
                jQuery('#team-holder .close-icon').on('click', function (e) {
                    jQuery('.team-load-content-holder').addClass("viceversa");
                    jQuery('.member-holder').css('display', 'block');
                    setTimeout(function () {
                        jQuery('#mcw-' + memberID).removeClass('show');
                        jQuery('.team-load-content-holder').removeClass('viceversa show');
                        jQuery('.member-holder').removeClass('hide');
                    }, 300);
                    // setTimeout(function () {
                    //    jQuery('html, body').animate({scrollTop: jQuery('#team-holder').offset().top - 150}, 400);
                    // }, 500);
                });
            });
        }
    });
    return false;
}

var portfolioItemContentLoadOnClick = function () {
    jQuery('.ajax-portfolio').on('click', function (e) {
        e.preventDefault();
        var portfolioItemID = jQuery(this).data('id');
        jQuery(this).addClass('animate-plus');
        if (jQuery("#pcw-" + portfolioItemID).length) //Check if is allready loaded
        {
            jQuery('html, body').animate({scrollTop: jQuery('#portfolio-wrapper').offset().top - 150}, 400);
            setTimeout(function () {
                jQuery('#portfolio-grid, .more-posts-portfolio-holder').addClass('hide');
                setTimeout(function () {
                    jQuery("#pcw-" + portfolioItemID).addClass('show');
                    jQuery('.portfolio-load-content-holder').addClass('show');
                    jQuery('.ajax-portfolio').removeClass('animate-plus');
                    jQuery('#portfolio-grid, .more-posts-portfolio-holder').hide();
                }, 300);
            }, 500);
        } else {
            loadPortfolioItemContent(portfolioItemID);
        }
    });
}

function loadPortfolioItemContent(portfolioItemID) {
    jQuery.ajax({
        url: jQuery('.ajax-portfolio[data-id="' + portfolioItemID + '"]').attr('href'),
        type: 'POST',
        success: function (html) {
            var getPortfolioItemHtml = jQuery(html).find(".portfolio-item-wrapper").html();
            jQuery('.portfolio-load-content-holder').append('<div id="pcw-' + portfolioItemID + '" class="portfolio-content-wrapper">' + getPortfolioItemHtml + '</div>');
            if (!jQuery("#pcw-" + portfolioItemID + " .close-icon").length) {
                jQuery("#pcw-" + portfolioItemID).prepend('<div class="close-icon"></div>');
            }
            jQuery('html, body').animate({scrollTop: jQuery('#portfolio-wrapper').offset().top - 150}, 400);
            setTimeout(function () {
                jQuery("#pcw-" + portfolioItemID).imagesLoaded(function () {
                    verticalSkills();
                    imageSliderSettings();
                    jQuery(".site-content").fitVids(); //Fit Video
                    jQuery('#portfolio-grid, .more-posts-portfolio-holder').addClass('hide');
                    setTimeout(function () {
                        jQuery("#pcw-" + portfolioItemID).addClass('show');
                        jQuery('.portfolio-load-content-holder').addClass('show');
                        jQuery('.ajax-portfolio').removeClass('animate-plus');
                        jQuery('#portfolio-grid').hide();
                    }, 300);
                    jQuery('.close-icon').on('click', function (e) {
                        var portfolioReturnItemID = jQuery(this).closest('.portfolio-content-wrapper').attr("id").split("-")[1];
                        jQuery('.portfolio-load-content-holder').addClass("viceversa");
                        jQuery('#portfolio-grid, .more-posts-portfolio-holder').css('display', 'block');
                        setTimeout(function () {
                            jQuery('#pcw-' + portfolioReturnItemID).removeClass('show');
                            jQuery('.portfolio-load-content-holder').removeClass('viceversa show');
                            jQuery('#portfolio-grid, .more-posts-portfolio-holder').removeClass('hide');
                        }, 300);
                        setTimeout(function () {
                            jQuery('html, body').animate({scrollTop: jQuery('#p-item-' + portfolioReturnItemID).offset().top - 150}, 400);
                        }, 500);
                    });
                });
            }, 500);
        }
    });
    return false;
}

function setPrettyPhoto() {
    jQuery('a[data-rel]').each(function () {
        jQuery(this).attr('rel', jQuery(this).data('rel'));
    });
    jQuery("a[rel^='prettyPhoto']").prettyPhoto({
        slideshow: false, /* false OR interval time in ms */
        overlay_gallery: false, /* If set to true, a gallery will overlay the fullscreen image on mouse over */
        default_width: 1280,
        default_height: 720,
        deeplinking: false,
        social_tools: false,
        iframe_markup: '<iframe src ="{path}" width="{width}" height="{height}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'
    });
}

function isotopeSetUp() {
    jQuery('.grid').isotope({
        itemSelector: '.grid-item',
        percentPosition: true,
        masonry: {
            columnWidth: '.grid-sizer',
            gutter: '.gutter-sizer'
        }
    });
}

function is_touch_device() {
    return !!('ontouchstart' in window);
}