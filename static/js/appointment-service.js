/**
 * Imza Appointment Service
 * A reusable module for handling weekly calendar reservations.
 * Author: Antigravity AI
 */

class ImzaAppointmentService {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.facilityId = options.facilityId || 'gym';
        this.apiBase = options.apiBase || '/api/neighborhood';
        this.onSelect = options.onSelect || null;
        this.onBooked = options.onBooked || null;
        
        this.selectedDate = null;
        this.selectedTime = null;
        this.routeData = [];
        this.weekDates = [];
    }

    async init() {
        this.calculateWeekDates();
        return this.loadCalendar();
    }

    calculateWeekDates() {
        const today = new Date();
        const dayOfWeek = today.getDay(); // 0 is Sunday
        const diff = today.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1); // Adjust to Monday
        const monday = new Date(today.setDate(diff));
        
        this.weekDates = [];
        for (let i = 0; i < 7; i++) {
            const date = new Date(monday);
            date.setDate(monday.getDate() + i);
            this.weekDates.push(date.toISOString().split('T')[0]);
        }
    }

    async loadCalendar(facilityId = null) {
        if (facilityId) this.facilityId = facilityId;
        
        const container = document.getElementById(this.containerId);
        if (!container) return;

        container.innerHTML = '<div class="col-span-7 flex justify-center py-4 text-gold"><i class="fa-solid fa-spinner fa-spin"></i></div>';
        
        const startDate = this.weekDates[0];
        const endDate = this.weekDates[6];

        try {
            const res = await fetch(`${this.apiBase}/reservations/calendar?facility_id=${this.facilityId}&start_date=${startDate}&end_date=${endDate}`);
            const booked = await res.json();
            this.render(booked);
        } catch (error) {
            console.error('Calendar load error:', error);
            container.innerHTML = '<div class="col-span-7 py-2 text-red-400 text-center">Takvim yüklenemedi</div>';
        }
    }

    render(booked) {
        const container = document.getElementById(this.containerId);
        let html = '';
        
        // Headers
        const days = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'];
        this.weekDates.forEach((date, i) => {
            const dayNum = date.split('-')[2];
            html += `
                <div class="flex flex-col items-center mb-2">
                    <span class="text-[8px] opacity-50 uppercase">${days[i]}</span>
                    <span class="font-bold text-white">${dayNum}</span>
                </div>
            `;
        });

        // Slots (09:00 - 17:00)
        const slots = ['09:00', '11:00', '13:00', '15:00', '17:00'];
        slots.forEach(time => {
            this.weekDates.forEach(date => {
                const isBooked = booked.find(b => b.reservation_date === date && b.time_slot === time);
                const isPast = new Date(`${date} ${time}`) < new Date();
                
                let statusClass = 'bg-white/5 border-white/5 text-gray-400 hover:border-gold cursor-pointer';
                let onclick = `window.imzaAppService.selectSlot('${date}', '${time}')`;
                
                if (isBooked) {
                    statusClass = 'bg-red-500/20 border-red-500/30 text-red-400 cursor-not-allowed';
                    onclick = '';
                } else if (isPast) {
                    statusClass = 'bg-gray-500/10 border-transparent text-gray-600 cursor-not-allowed';
                    onclick = '';
                }

                html += `
                    <div id="slot-${date}-${time.replace(':','')}" 
                         ${onclick} 
                         class="p-1 border rounded text-center transition-all ${statusClass}">
                        ${time}
                    </div>
                `;
            });
        });

        container.innerHTML = html;
    }

    selectSlot(date, time) {
        const prevId = `slot-${this.selectedDate}-${this.selectedTime ? this.selectedTime.replace(':','') : ''}`;
        const prev = document.getElementById(prevId);
        if (prev) prev.classList.remove('bg-gold', 'text-navy', 'border-gold');

        this.selectedDate = date;
        this.selectedTime = time;

        const current = document.getElementById(`slot-${date}-${time.replace(':','')}`);
        if (current) {
            current.classList.add('bg-gold', 'text-navy', 'border-gold');
        }

        if (this.onSelect) this.onSelect(date, time);
    }

    async book(userName = 'Mahalle Sakini') {
        if (!this.selectedDate || !this.selectedTime) return { success: false, error: 'Slot seçilmedi' };

        try {
            const response = await fetch(`${this.apiBase}/reservations`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    facility_id: this.facilityId,
                    date: this.selectedDate,
                    time: this.selectedTime,
                    name: userName
                })
            });
            
            if (response.ok) {
                this.loadCalendar(); // Refresh
                if (this.onBooked) this.onBooked();
                return { success: true };
            }
            return { success: false, error: 'API hatası' };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }
}

// Global instance for easy access in templates
window.ImzaAppointmentService = ImzaAppointmentService;
