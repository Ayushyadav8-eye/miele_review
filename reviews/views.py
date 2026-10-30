
from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import redirect, render

from .forms import ReviewForm
from .models import Review


def review_page(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you! Your feedback has been submitted."
            )
            return redirect("review_page")
        messages.error(
            request,
            "Please correct the errors below."
        )
    else:
        form = ReviewForm()

    stats = Review.objects.aggregate(
        total=Count("id"),
        average=Avg("rating"),
    )

    total_reviews = stats["total"] or 0
    average_rating = stats["average"] or 0

    rating_counts = {
        row["rating"]: row["count"]
        for row in Review.objects.values("rating").annotate(
            count=Count("id")
        )
    }

    rating_breakdown = []

    for rating in range(5, 0, -1):
        count = rating_counts.get(rating, 0)

        percentage = (
            round(count * 100 / total_reviews)
            if total_reviews else 0
        )

        rating_breakdown.append({
            "rating": rating,
            "count": count,
            "percentage": percentage,
        })

    context = {
        "form": form,
        "total_reviews": total_reviews,
        "average_rating": round(average_rating, 1),
        "rating_breakdown": rating_breakdown,
    }

    return render(
        request,
        "reviews/review.html",
        context,
    )
