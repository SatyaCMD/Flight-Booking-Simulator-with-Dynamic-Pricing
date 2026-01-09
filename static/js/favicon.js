const favicon = document.createElement('link');
favicon.rel = 'icon';
favicon.href = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">✈️</text></svg>';
document.head.appendChild(favicon);

const link = document.createElement('link');
link.rel = 'icon';
link.href = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E2%9C%88%EF%B8%8F%3C/text%3E%3C/svg%3E";
document.head.appendChild(link);

const airplaneFavicon = document.createElement('link');
airplaneFavicon.rel = 'icon';
airplaneFavicon.href = `data:image/svg+xml,
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>
  <text y='.9em' font-size='90' transform='rotate(45 50 50)'>✈️</text>
</svg>
`;
document.head.appendChild(airplaneFavicon);