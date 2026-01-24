// 전역 JavaScript 함수들

// 페이지 로드 시 애니메이션 효과
document.addEventListener('DOMContentLoaded', function() {
    // 카드 애니메이션
    const cards = document.querySelectorAll('.topic-card, .feature-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s, transform 0.5s';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // 스무스 스크롤
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// 숫자 입력 필드에 숫자만 입력되도록 제한
function restrictToNumbers(input) {
    input.addEventListener('input', function(e) {
        this.value = this.value.replace(/[^0-9.\-+()x²]/g, '');
    });
}

// Enter 키로 제출
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement && activeElement.classList.contains('answer-input')) {
            const checkButton = activeElement.parentElement.querySelector('.btn-primary');
            if (checkButton) {
                checkButton.click();
            }
        }
    }
});
