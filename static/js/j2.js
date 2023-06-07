$(function(){

    'use strict'
  
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
  
    // set active contact from list to show in desktop view by default
    if(window.matchMedia('(min-width: 992px)').matches) {
      $('.contact-list .media:first-of-type').addClass('active');
    }
  
  
    const contactSidebar = new PerfectScrollbar('.contact-sidebar-body', {
      suppressScrollX: true
    });
  
    new PerfectScrollbar('.contact-content-body', {
      suppressScrollX: true
    });
  
    new PerfectScrollbar('.contact-content-sidebar', {
      suppressScrollX: true
    });
  
    $('.contact-navleft .nav-link').on('shown.bs.tab', function(e) {
      contactSidebar.update()
    })
  
    // UI INTERACTION
    $('.contact-list .media').on('click', function(e) {
      e.preventDefault();
  
      $('.contact-list .media').removeClass('active');
      $(this).addClass('active');
  
      var cName = $(this).find('h6').text();
      $('#contactName').text(cName);
  
      var cAvatar = $(this).find('.avatar').clone();
  
      cAvatar.removeClass (function (index, className) {
        return (className.match (/(^|\s)avatar-\S+/g) || []).join(' ');
      });
      cAvatar.addClass('avatar-xl');
  
      $('#contactAvatar .avatar').replaceWith(cAvatar);
  
  
      // showing contact information when clicking one of the list
      // for mobile interaction only
      if(window.matchMedia('(max-width: 991px)').matches) {
        $('body').addClass('contact-content-show');
        $('body').removeClass('contact-content-visible');
  
        $('#mainMenuOpen').addClass('d-none');
        $('#contactContentHide').removeClass('d-none');
      }
    })
  
  
    // going back to contact list
    // for mobile interaction only
    $('#contactContentHide').on('click touch', function(e){
      e.preventDefault();
  
      $('body').removeClass('contact-content-show contact-options-show');
      $('body').addClass('contact-content-visible');
  
      $('#mainMenuOpen').removeClass('d-none');
      $(this).addClass('d-none');
    });
  
    $('#contactOptions').on('click', function(e){
      e.preventDefault();
      $('body').toggleClass('contact-options-show');
    })
  
    $(window).resize(function(){
      $('body').removeClass('contact-options-show');
    })
  
  })
  
  
  
  $(function(){
    'use strict'
  
    feather.replace();
  
    ////////// NAVBAR //////////
  
    // Initialize PerfectScrollbar of navbar menu for mobile only
    if(window.matchMedia('(max-width: 991px)').matches) {
      const psNavbar = new PerfectScrollbar('#navbarMenu', {
        suppressScrollX: true
      });
    }
  
    // Showing sub-menu of active menu on navbar when mobile
    function showNavbarActiveSub() {
      if(window.matchMedia('(max-width: 991px)').matches) {
        $('#navbarMenu .active').addClass('show');
      } else {
        $('#navbarMenu .active').removeClass('show');
      }
    }
  
    showNavbarActiveSub()
    $(window).resize(function(){
      showNavbarActiveSub()
    })
  
    // Initialize backdrop for overlay purpose
    $('body').append('<div class="backdrop"></div>');
  
  
    // Showing sub menu of navbar menu while hiding other siblings
    $('.navbar-menu .with-sub .nav-link').on('click', function(e){
      e.preventDefault();
      $(this).parent().toggleClass('show');
      $(this).parent().siblings().removeClass('show');
  
      if(window.matchMedia('(max-width: 991px)').matches) {
        psNavbar.update();
      }
    })
  
    // Closing dropdown menu of navbar menu
    $(document).on('click touchstart', function(e){
      e.stopPropagation();
  
      // closing nav sub menu of header when clicking outside of it
      if(window.matchMedia('(min-width: 992px)').matches) {
        var navTarg = $(e.target).closest('.navbar-menu .nav-item').length;
        if(!navTarg) {
          $('.navbar-header .nav-item').removeClass('show');
        }
      }
    })
  
    $('#mainMenuClose').on('click', function(e){
      e.preventDefault();
      $('body').removeClass('navbar-nav-show');
    });
  
    $('#sidebarMenuOpen').on('click', function(e){
      e.preventDefault();
      $('body').addClass('sidebar-show');
    })
  
    // Navbar Search
    $('#navbarSearch').on('click', function(e){
      e.preventDefault();
      $('.navbar-search').addClass('visible');
      $('.backdrop').addClass('show');
    })
  
    $('#navbarSearchClose').on('click', function(e){
      e.preventDefault();
      $('.navbar-search').removeClass('visible');
      $('.backdrop').removeClass('show');
    })
  
  
  
    ////////// SIDEBAR //////////
  
    // Initialize PerfectScrollbar for sidebar menu
    if($('#sidebarMenu').length) {
      const psSidebar = new PerfectScrollbar('#sidebarMenu', {
        suppressScrollX: true
      });
  
  
      // Showing sub menu in sidebar
      $('.sidebar-nav .with-sub').on('click', function(e){
        e.preventDefault();
        $(this).parent().toggleClass('show');
  
        psSidebar.update();
      })
    }
  
  
    $('#mainMenuOpen').on('click touchstart', function(e){
      e.preventDefault();
      $('body').addClass('navbar-nav-show');
    })
  
    $('#sidebarMenuClose').on('click', function(e){
      e.preventDefault();
      $('body').removeClass('sidebar-show');
    })
  
    // hide sidebar when clicking outside of it
    $(document).on('click touchstart', function(e){
      e.stopPropagation();
  
      // closing of sidebar menu when clicking outside of it
      if(!$(e.target).closest('.burger-menu').length) {
        var sb = $(e.target).closest('.sidebar').length;
        var nb = $(e.target).closest('.navbar-menu-wrapper').length;
        if(!sb && !nb) {
          if($('body').hasClass('navbar-nav-show')) {
            $('body').removeClass('navbar-nav-show');
          } else {
            $('body').removeClass('sidebar-show');
          }
        }
      }
    });
  
  })
  