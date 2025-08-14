from django.shortcuts import render

# ...existing imports...

def sentiment_chart_page(request):
    return render(request, 'sentiment_chart.html')

# ...existing code...