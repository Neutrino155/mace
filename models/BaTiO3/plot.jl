using Plots, DelimitedFiles, Measures

mu_data = readdlm("DATA_mu.txt")
mu_mace = readdlm("MACE_mu.txt")

mu_lims = [(minimum(hcat(mu_data[:,i], mu_mace[:,i])), maximum(hcat(mu_data[:,i], mu_mace[:,i]))) .* 1.1 for i in 1:3] 

for i in 1:3
    @eval $(Symbol("p_mu_$i")) = $(scatter(mu_data[:,i], mu_mace[:,i], ylims=mu_lims[i], xlims=mu_lims[i], legend=false, title="Dipole $i", framestyle=:box, size=(300,300)))
    plot!(LinRange(mu_lims[i]..., 100), LinRange(mu_lims[i]..., 100), linestyle=:dash, color=:red, linewidth=2)
end

p_mu = plot(p_mu_1, p_mu_2, p_mu_3, xlabel="Data Dipole (eÅ)", ylabel="Mace Dipole (eÅ)", layout=grid(1,3, widths=(3/9,3/9,3/9)), size=(1600,500), margin=10mm)

savefig(p_mu, "dipole_comparison_plot.png")

alpha_data = readdlm("DATA_alpha.txt")
alpha_mace = readdlm("MACE_alpha.txt")

alpha_lims = [(minimum(hcat(alpha_data[:,i], alpha_mace[:,i])), maximum(hcat(alpha_data[:,i], alpha_mace[:,i]))) .* 1.1 for i in 1:9] 

for i in 1:9
    @eval $(Symbol("p_alpha_$i")) = $(scatter(alpha_data[:,i], alpha_mace[:,i], ylims=alpha_lims[i], xlims=alpha_lims[i], legend=false, title="Polarizability $i", framestyle=:box, size=(300,300)))
    plot!(LinRange(alpha_lims[i]..., 100), LinRange(alpha_lims[i]..., 100), linestyle=:dash, color=:red, linewidth=2)
end

p_alpha = plot(p_alpha_1, p_alpha_2, p_alpha_3, p_alpha_4, p_alpha_5, p_alpha_6, p_alpha_7, p_alpha_8, p_alpha_9, xlabel="Data polarizability (eÅ²/V)", ylabel="Mace Polarizability (eÅ²/V)", layout=9, size=(1700,1700), margin=10mm, markerstrokewidth=0.5)

savefig(p_alpha, "polarizability_comparison_plot.png")