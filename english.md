---
layout: default
permalink: /english/
---
<div class="home">
    
<article class="post">

  <div class="post-content">
    <div class="section group">

    <div class="col span_1_of_2">
      <div class="info_section">
        <h1 class="info_section__title">Important news</h1>
        {% assign main_category_posts = site.categories[site.main_category] %}
        {%
          include functions/post-list_en.html
          posts=main_category_posts
          limit=5
        %}
        <a href="News">All news</a>
      </div>
    </div>

    <div class="col span_1_of_2">
        <div class="info_section">
          <h1 class="info_section__title">What is AS?</h1>
          {% capture index_content %}{% include index_content_en.md %}{% endcapture %}
          {{ index_content | markdownify }}
        </div>

        <div class="info_section">
          <h1 class="info_section__title">Incoming events</h1>
          <ul id="event-list" class="event_list">
          </ul>
          <ul id="event-list-2" class="event_list">
          </ul>

          <a href="{{ "/events.html" | absolute_url }}">
            All events
          </a>
        </div>
    </div>

    </div>
  </div>

</article>

</div>

<script src="{{ "/static/js/moment.min.js" | absolute_url }}"></script>
<script src="{{ "/static/js/format-google-calendar.js" | absolute_url }}"></script>
<script type="text/javascript">
  var startDate = new Date();
  var endDate = new Date();
  startDate.setDate(startDate.getDate() - 1);
  endDate.setFullYear(startDate.getFullYear() + 2);
  var timestamp_start = startDate.toISOString();
  var timestamp_end = endDate.toISOString();

  formatGoogleCalendar.init({
    calendarUrl: 'https://www.googleapis.com/calendar/v3/calendars/as.tiedottaja@gmail.com/events?key=AIzaSyCJrtmGOeEFAq912lwijvCmKR33SAtC_qo',
    past: false,
    upcoming: true,
    sameDayTimes: true,
    dayNames: true,
    pastTopN: -1,
    upcomingTopN: 5,
    recurringEvents: true,
    itemsTagName: 'li',
    upcomingSelector: '#event-list',
    pastSelector: '#event-list-2',
    upcomingHeading: '',
    pastHeading: '',
    format: ['*summary*', '*date*', '*description*'],
    timeMin: timestamp_start,
    timeMax: timestamp_end
  });
</script>
